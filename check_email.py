import xml.etree.ElementTree as ET
import re

def check_emails_in_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        found_email = False

        for author in article.findall(".//Author"):
            affil_node = author.find("AffiliationInfo/Affiliation")
            affil = affil_node.text if affil_node is not None else ""

            emails = re.findall(r"[\w\.-]+@[\w\.-]+", affil)
            if emails:
                print("PMID {} — '{}' has email(s): {}".format(pmid,title,emails))
                found_email = True
                break  # Stop after finding first email in this article

        if not found_email:
            print("PMID {} — '{}' has NO emails found.".format(pmid,title))

# Usage
check_emails_in_xml("pubmed_output.xml")