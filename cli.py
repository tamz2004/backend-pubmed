"""Command line interface for *get-papers-list* script."""
import argparse
import sys
from typing import List
from pubmed import search_and_filter
from pubmed.writer import write_csv, HEADERS

def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="get-papers-list",
        description="Fetch PubMed papers with at least one pharma/biotech author.",
    )
    parser.add_argument("query", help="PubMed search query (in quotes).")
    parser.add_argument(
        "-d", "--debug", action="store_true", help="Enable verbose debug output."
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="FILENAME",
        help="Write CSV output to file instead of stdout.",
    )
    return parser.parse_args(argv)

def main(argv: List[str] | None = None) -> None:
    args = parse_args(argv)
    rows = search_and_filter(args.query, debug=args.debug)

    if args.file:
        write_csv(rows, args.file)
        if args.debug:
            print(f"Wrote {len(rows)} row(s) to {args.file}")
    else:
        # Print to stdout as CSV
        import csv
        import sys
        writer = csv.DictWriter(sys.stdout, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

if __name__ == "__main__":
    main()
