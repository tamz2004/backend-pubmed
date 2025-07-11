from typing import List, Dict, Any
import xml.etree.ElementTree as ET
from Bio import Entrez

Entrez.email = "your.email@example.com" #Replace with your email address

def search_pubmed(*, query: str, retmax: int = 200, debug: bool=False) -> List[str]:
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    result = Entrez.read(handle)
    handle.close()
    if debug:
        print("esearch result keys:", result.keys())
    return result["IdList"]

def _parse_record_xml(article_xml: str) -> Dict[str, Any]:
    root = ET.fromstring(article_xml)
    article = {}

    pmid_el = root.find(".//PMID")
    article["pmid"] = pmid_el.text if pmid_el is not None else None

    title_el = root.find(".//ArticleTitle")
    article["title"] = "".join(title_el.itertext()).strip() if title_el is not None else None

    date_text = None
    date_el = root.find(".//ArticleDate") or root.find(".//PubDate")
    if date_el is not None:
        year = date_el.findtext("Year")
        month = date_el.findtext("Month")
        day = date_el.findtext("Day")
        date_text = "-".join(filter(None, [year, month, day]))
    article["date"] = date_text

    article["authors"] = []
    for author in root.findall(".//Author"):
        last = author.findtext("LastName") or ""
        fore = author.findtext("ForeName") or ""
        name = f"{fore} {last}".strip()
        affiliations = [aff.text.strip() for aff in author.findall(".//Affiliation") if aff.text]
        article["authors"].append({"name": name, "affiliations": affiliations})

    return article

def fetch_details(*, pmids: List[str], batch_size: int = 200, debug: bool=False) -> List[dict]:
    all_records = []
    for i in range(0, len(pmids), batch_size):
        batch_pmids = pmids[i:i+batch_size]
        try:
            if debug:
                print(f"Fetching details for PMIDs {batch_pmids[0]}..{batch_pmids[-1]}")
            handle = Entrez.efetch(db="pubmed", id=",".join(batch_pmids), rettype="xml")
            data = handle.read().decode("utf-8")
            handle.close()
            for article_xml in data.split("<PubmedArticle>")[1:]:
                article_xml = "<PubmedArticle>" + article_xml.split("</PubmedArticle>")[0] + "</PubmedArticle>"
                parsed = _parse_record_xml(article_xml)
                all_records.append(parsed)
        except Exception as e:
            if debug:
                print(f"Error fetching details for PMIDs {batch_pmids[0]}..{batch_pmids[-1]}: {e}")
            continue
    return all_records
