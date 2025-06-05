import os
import shutil

from name_matching.db import ChromaDB


def setup_module() -> None:
    if os.path.exists("./chroma_store"):
        shutil.rmtree("./chroma_store")


def teardown_module() -> None:
    if os.path.exists("./chroma_store"):
        shutil.rmtree("./chroma_store")


def test_chromadb_basic_persistence():
    db = ChromaDB()
    db.add_names_batch(["Alice", "Bob", "Charlie"])
    assert db.count() == 3

    results = db.query_embedding("Alice", top_k=1, threshold=0.0)
    assert "Alice" in results

    db2 = ChromaDB()
    assert db2.count() == 3


def test_collection_management():
    db = ChromaDB()
    collections = db.list_collections()
    assert any(c == "names" for c in collections)

    db.delete_collection("names")
    collections_after = db.list_collections()
    assert "names" not in collections_after
