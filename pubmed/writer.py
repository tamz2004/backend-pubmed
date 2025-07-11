"""CSV writing helpers."""
import csv
from typing import List, Dict, Any, Iterable

HEADERS = [
    "PubmedID",
    "Title",
    "Publication Date",
    "Non-academic Author(s)",
    "Company Affiliation(s)",
    "Corresponding Author Email"
]

def records_to_rows(record: Dict[str, Any]) -> Dict[str, str]:
    """Map internal record structure to CSV row dict."""
    return {
        "PubmedID": record.get("pmid", ""),
        "Title": record.get("title", ""),
        "Publication Date": record.get("date", ""),
        "Non-academic Author(s)": record.get("non_academic_authors", ""),
        "Company Affiliation(s)": record.get("companies", ""),
        "Corresponding Author Email": record.get("corresponding_email", "")
    }

def write_csv(rows: Iterable[Dict[str, str]], file_path: str) -> None:
    with open(file_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=HEADERS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
