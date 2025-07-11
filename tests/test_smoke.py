from importlib import import_module

def test_import():
    mod = import_module("pubmed")
    assert hasattr(mod, "search_and_filter")
