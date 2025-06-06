from __future__ import annotations

from faker import Faker

from .db import ChromaDB


def load_fake_names(
    count: int,
    *,
    path: str = "./chroma_store",
    collection_name: str = "names",
) -> ChromaDB:
    """Generate ``count`` fake names and store them in a :class:`ChromaDB`.

    Parameters
    ----------
    count:
        Number of fake names to generate.
    path:
        Optional filesystem path for the persistent Chroma store.
    Returns
    -------
    ChromaDB
        The database instance containing the generated names.
    """
    fake = Faker()
    names = [f"{fake.first_name()} {fake.last_name()}" for _ in range(count)]
    db = ChromaDB(path=path, collection_name=collection_name)
    db.add_names_batch(names)
    return db
