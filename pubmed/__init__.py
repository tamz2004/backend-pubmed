from typing import List, Dict
from .api import search_pubmed, fetch_details
from .filter import filter_records
from .writer import records_to_rows

__all__ = ["search_and_filter"]

def search_and_filter(query: str, *, debug: bool=False, retmax: int=200) -> List[Dict[str, str]]:
   
    pmids = search_pubmed(query=query, retmax=retmax, debug=debug)
    if debug:
        print(f"Fetched {len(pmids)} PMID(s).")

    records = fetch_details(pmids=pmids, debug=debug)
    if debug:
        print(f"Fetched {len(records)} record(s) details.")

    filtered = filter_records(records, debug=debug)
    return [records_to_rows(r) for r in filtered]
