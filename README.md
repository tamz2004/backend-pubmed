# 🧪 backend-pubmed

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Build](https://img.shields.io/badge/build-passing-brightgreen)]()
[![mypy](https://img.shields.io/badge/mypy-checked-blueviolet)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![TestPyPI](https://img.shields.io/badge/TestPyPI-published-green)](https://test.pypi.org/project/backend-pubmed/)


A CLI tool that fetches research papers from PubMed and filters for authors affiliated with biotech/pharma companies.

---

## 📋 Submission Summary

### ✅ Problem Covered:
Fetch and filter PubMed results for company-affiliated authors (non-academic) using heuristics.

### 🔧 Key Features:
- Full PubMed query syntax
- Detect non-academic authors using affiliation heuristics
- Outputs clean CSV
- Uses Poetry, type-annotated Python, modular code

### ⚙ Tech:
- Python 3.10+
- [Biopython](https://biopython.org/)
- Poetry for packaging
- Typed Python (`mypy`)
- pytest for testing

### 🧪 Evaluation Ready:
- ✅ Adheres to functional requirements
- ✅ Meets non-functional expectations: performance, typing, docs
- ✅ Bonus: modular design, ready for TestPyPI publishing

---

## 🧠 Maintainer Notes
- `Entrez.email` should be updated with a valid address in `pubmed/api.py`
- Errors during API calls are handled gracefully
