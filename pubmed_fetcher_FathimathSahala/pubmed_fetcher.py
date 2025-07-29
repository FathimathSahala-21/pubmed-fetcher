import argparse
import logging
import requests
import csv
import re
from typing import List, Tuple
from xml.etree import ElementTree as ET

ACADEMIC_KEYWORDS = ["university", "college", "institute", "school", "department"]
COMPANY_KEYWORDS = ["pharma", "biotech", "inc", "ltd", "llc", "corp"]

def fetch_pubmed_ids(query: str, debug: bool = False, api_key: str = None) -> List[str]:
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": "100"
    }

    if api_key:
        params["api_key"] = api_key

    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, params=params, headers=headers, allow_redirects=False)

        if debug:
            print("[DEBUG] ESearch URL:", r.url)
            print("[DEBUG] Status Code:", r.status_code)
            print("[DEBUG] Response Text:", r.text)

        if r.status_code == 302:
            raise RuntimeError("Redirected to another domain. PubMed may be blocking your request. Try again later or use a VPN.")

        r.raise_for_status()

        return r.json().get("esearchresult", {}).get("idlist", [])

    except requests.exceptions.HTTPError as e:
        logging.error("HTTP error occurred: {}".format(e))
        return []
    except Exception as e:
        logging.error("Unexpected error occurred: {}".format(e))
        return []


def fetch_pubmed_details(ids: List[str], debug: bool = False) -> str:
    ids_str = ",".join(ids)
    params = {
        "db": "pubmed",
        "id": ids_str,
        "retmode": "xml",
       # "api_key": "47d23b62816a47e5ad35b084b41a90a3"  # Replace with your own key later
    }
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    r = requests.get(url, params=params, headers=headers, allow_redirects=False)

    if debug:
        print("[DEBUG] EFetch URL:", r.url)
    r.raise_for_status()
    return r.text

def is_non_academic(affiliation: str) -> bool:
    affil = affiliation.lower()
    return not any(k in affil for k in ACADEMIC_KEYWORDS) and any(k in affil for k in COMPANY_KEYWORDS)


def extract_paper_info(xml_data: str) -> List[Tuple[str, str, str, List[str], List[str], str]]:

    root = ET.fromstring(xml_data)
    results = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")

        # Parse publication date
        date_node = article.find(".//PubDate")
        pub_date = ""
        if date_node is not None:
            year = date_node.findtext("Year") or ""
            month = date_node.findtext("Month") or ""
            day = date_node.findtext("Day") or ""
            pub_date = "{}-{}-{}".format(year, month, day)

        authors = article.findall(".//Author")
        non_acad_authors = []
        company_affiliations = []
        collected_emails = []  # reset per article

        for author in authors:
            affil_node = author.find("AffiliationInfo/Affiliation")
            if affil_node is not None:
                affil = affil_node.text or ""

                # Collect emails from all affiliations
                emails = re.findall(r"[\w\.-]+@[\w\.-]+", affil)
                collected_emails.extend(emails)

                if is_non_academic(affil):
                    lastname = author.findtext("LastName") or ""
                    firstname = author.findtext("ForeName") or ""
                    name = "{} {}".format(firstname, lastname).strip()
                    non_acad_authors.append(name)
                    company_affiliations.append(affil)

        # Select email only after going through all authors
        email = collected_emails[0] if collected_emails else ""

        if non_acad_authors:
            results.append((pmid, title, pub_date, non_acad_authors, company_affiliations, email))

    return results


def save_to_csv(filename: str, data: List[Tuple[str, str, str, List[str], List[str], str]]) -> None:
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["PubmedID", "Title", "Publication Date", "Non-academic Author(s)", "Company Affiliation(s)", "Corresponding Author Email"])
        for row in data:
            writer.writerow([
                row[0],
                row[1],
                row[2],
                "; ".join(row[3]),
                "; ".join(row[4]),
                row[5]
            ])





