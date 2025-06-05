import os
import shutil

from name_matching.loader import load_fake_names


def setup_module() -> None:
    if os.path.exists("./chroma_store"):
        shutil.rmtree("./chroma_store")


def teardown_module() -> None:
    if os.path.exists("./chroma_store"):
        shutil.rmtree("./chroma_store")


def test_load_fake_names_creates_db(tmp_path):
    db_path = tmp_path / "store"
    db = load_fake_names(5, path=str(db_path))
    assert db.count() == 5
