"""Filtering and heuristics for identifying non‑academic authors."""
import re
from typing import List, Dict, Tuple, Any

_ACADEMIC_KEYWORDS = re.compile(
    r"""(
        university|college|institute|center|centre|hospital|
        school|department|dept\.|faculty|laboratory|research\s*centre
    )""", re.I | re.X
)

_COMPANY_KEYWORDS = re.compile(
    r"""(
        pharma|pharmaceuticals?|therapeutics|biosciences?|biotech|
        laboratories|ltd\.?|inc\.?|llc|corp\.?|ag|gmbh|sas|plc
    )""", re.I | re.X
)

def _is_academic(aff: str) -> bool:
    return bool(_ACADEMIC_KEYWORDS.search(aff))

def _is_company(aff: str) -> bool:
    return bool(_COMPANY_KEYWORDS.search(aff))

def _extract_email(text: str) -> str | None:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return match.group(0) if match else None

def analyse_author(author: dict) -> tuple[bool, list[str], str | None]:
    """Return tuple (is_non_academic, companies, email) for *author*."""
    companies: list[str] = []
    email: str | None = None
    for aff in author.get("affiliations", []):
        if not _is_academic(aff) and _is_company(aff):
            companies.append(aff)
        # capture email anywhere
        if email is None:
            email = _extract_email(aff)
    is_non_academic = bool(companies)
    return is_non_academic, companies, email

def filter_records(records: List[Dict[str, Any]], *, debug: bool=False) -> List[Dict[str, Any]]:
    """Keep records with ≥1 non‑academic author, augment with fields."""
    filtered = []
    for rec in records:
        non_academic_authors = []
        companies: set[str] = set()
        corr_email: str | None = None

        for author in rec.get("authors", []):
            is_na, comps, email = analyse_author(author)
            if is_na:
                non_academic_authors.append(author["name"])
                companies.update(comps)
            if corr_email is None and email:
                corr_email = email

        if non_academic_authors:
            rec["non_academic_authors"] = "; ".join(non_academic_authors)
            rec["companies"] = "; ".join(companies)
            rec["corresponding_email"] = corr_email or ""
            filtered.append(rec)
            if debug:
                print(f"PMID {rec['pmid']} kept – {len(non_academic_authors)} non‑academic author(s).")
        elif debug:
            print(f"PMID {rec['pmid']} skipped – no non‑academic authors.")
    return filtered
