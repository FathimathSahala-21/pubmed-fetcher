# PubMed Fetcher

A Python tool to fetch research papers from PubMed based on user queries, identify papers with authors affiliated with pharmaceutical or biotech companies, and output the results as a CSV file.

---

## Features

- Fetch papers using PubMed API with full query syntax support.
- Identify non-academic authors using heuristics on affiliation strings.
- Extract relevant paper information: PubMed ID, title, publication date, non-academic authors, company affiliations, and corresponding author email.
- Command-line interface with options for debug logging and specifying output file.
- Modular design: core functionality separated from CLI interface.
- Uses Poetry for dependency management and packaging.
- Executable command `get-papers-list` provided via Poetry.

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/FathimathSahala-21/pubmed-fetcher.git
   cd pubmed-fetcher
   ```

2. **Install dependencies via Poetry:**

   Make sure you have Poetry installed globally. If not, install it following [Poetry Installation Guide](https://python-poetry.org/docs/#installation).

   Then run:

   ```bash
   poetry install
   ```

---

## Usage

Run the command via Poetry:

```bash
poetry run get-papers-list "your PubMed query" --file results.csv --debug
```
---

## Publishing and Testing

This package is published on [TestPyPI](https://test.pypi.org/) as a testing ground before publishing to the official PyPI.

To install the package directly from TestPyPI, run:

```bash
pip install --index-url https://test.pypi.org/simple/ pubmed_fetcher_FathimathSahala
```
---
### Options

- `query` (positional): PubMed search query using full PubMed syntax.
- `-f, --file` (optional): Specify output CSV filename. If omitted, output is printed to console.
- `-d, --debug` (optional): Enable debug mode for verbose logging.
- `-h, --help`: Show usage instructions.

---

## Code Organization

- `pubmed_fetcher_FathimathSahala/` — Python package with core modules:
  - `pubmed_fetcher.py`: Core functions to fetch, parse, and filter PubMed papers.
  - `cli.py`: Command-line interface that handles arguments and calls core functions.
- `pyproject.toml` — Poetry configuration, dependencies, and CLI entry points.
- `README.md` — This documentation file.

---

## How it works

1. User provides a PubMed query.
2. The tool fetches matching paper IDs via PubMed's ESearch API.
3. Fetches detailed paper info via EFetch API.
4. Parses XML response to extract author affiliations and identifies non-academic authors based on keywords.
5. Saves the filtered results with required fields into a CSV file or prints to console.

---

## Dependencies and Tools

- [requests](https://requests.readthedocs.io/en/latest/) — HTTP requests to PubMed API.
- [Poetry](https://python-poetry.org/) — Dependency and packaging management.
- Python 3.8+ (tested with Python 3.13)
- Uses standard library modules like `argparse`, `csv`, `re`, and `xml.etree.ElementTree`.

---

## Notes

- Non-academic author detection uses simple keyword heuristics (e.g., excluding "university", "institute" and including "pharma", "biotech", etc.).
- Ensure you have a working internet connection to query the PubMed API.
- For large queries, consider using a PubMed API key to avoid rate limits.

---

## License

This project is licensed under the MIT License.

---

## Author

Fathimath Sahala — sahalazakariya18@gmail.com

---

## Example

Fetch papers related to cancer therapy and save results to `results.csv` with debug info:

```bash
poetry run get-papers-list "cancer therapy" --file results.csv --debug
```
