from __future__ import annotations

import hashlib
import math
import uuid
from collections import defaultdict

import chromadb

_clients: defaultdict[str, chromadb.ClientAPI] = defaultdict(chromadb.EphemeralClient)


def _embed(text: str) -> list[float]:
    """Create a deterministic embedding from a string using SHA256."""
    digest = hashlib.sha256(text.lower().encode("utf-8")).digest()
    return list(digest)


def _normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


class ChromaDB:
    """Wrapper around a Chroma collection using an in-memory client."""

    def __init__(self, path: str = "./chroma_store", collection_name: str = "names") -> None:
        self.client = _clients[path]
        self.collection_name = collection_name
        self.collection = self.client.get_or_create_collection(
            collection_name,
            metadata={"hnsw:space": "l2"},
        )

    def add_names_batch(self, names: list[str]) -> None:
        embeddings = [_normalize(_embed(n)) for n in names]
        ids = [str(uuid.uuid4()) for _ in names]
        self.collection.add(ids=ids, documents=names, embeddings=embeddings)

    def query_embedding(self, text: str, top_k: int, threshold: float) -> list[str]:
        query_embedding = [_normalize(_embed(text))]
        result = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k,
            include=["distances", "documents"],
        )
        docs = result["documents"][0]
        dists = result["distances"][0]
        matches: list[str] = []
        for doc, dist in zip(docs, dists, strict=False):
            cosine = 1 - dist / 2
            if cosine >= threshold:
                matches.append(doc)
        return matches

    def count(self) -> int:
        return self.collection.count()

    def delete_collection(self, name: str | None = None) -> None:
        if name is None:
            name = self.collection_name
        self.client.delete_collection(name)

    def list_collections(self) -> list[str]:
        return [c.name for c in self.client.list_collections()]
