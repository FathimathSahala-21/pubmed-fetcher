import argparse
import logging
from pubmed_fetcher_FathimathSahala.pubmed_fetcher import fetch_pubmed_ids, fetch_pubmed_details, extract_paper_info, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers with non-academic authors.")
    parser.add_argument("query", type=str, help="PubMed search query")
    parser.add_argument("-f", "--file", type=str, help="Output file to save CSV")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    ids = fetch_pubmed_ids(args.query, debug=args.debug)
    if not ids:
        print("No papers found for the query.")
        return

    xml_data = fetch_pubmed_details(ids, debug=args.debug)
    results = extract_paper_info(xml_data)

    output_filename = args.file or "results.csv"
    save_to_csv(output_filename, results)
    print("Results saved to {}".format(output_filename))

if __name__ == "__main__":
    main()
