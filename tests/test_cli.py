import os
import shutil

from name_matching import cli, db


def setup_module() -> None:
    if os.path.exists("./chroma_store"):
        shutil.rmtree("./chroma_store")


def teardown_module() -> None:
    if os.path.exists("./chroma_store"):
        shutil.rmtree("./chroma_store")


def test_load_command_creates_collection(capsys):
    cli.main(["load", "--count", "3", "--collection", "cli_test"])
    captured = capsys.readouterr()
    assert "Loaded 3" in captured.out

    db_instance = db.ChromaDB(collection_name="cli_test")
    assert db_instance.count() == 3


def test_match_command_returns_results(capsys):
    collection = "cli_match"
    db_instance = db.ChromaDB(collection_name=collection)
    db_instance.add_names_batch(["John Doe", "Jane Doe"])

    cli.main(
        [
            "match",
            "--name",
            "Jon Doe",
            "--type",
            "fuzzy",
            "--collection",
            collection,
        ]
    )
    captured = capsys.readouterr()
    assert "John Doe" in captured.out
