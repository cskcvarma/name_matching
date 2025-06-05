import hashlib
import math
import uuid

import chromadb


def _embed(text: str) -> list[float]:
    """Create a deterministic embedding from a string using SHA256."""
    digest = hashlib.sha256(text.lower().encode("utf-8")).digest()
    # Use the raw bytes as small-dimensional vector
    return list(digest)


def _normalize(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0:
        return vec
    return [v / norm for v in vec]


class ChromaDB:
    """Lightweight wrapper around a persistent Chroma collection."""

    def __init__(self, path: str = "./chroma_store") -> None:
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            "names",
            metadata={"hnsw:space": "l2"},
        )

    def add_names_batch(self, names: list[str]) -> None:
        """Add a batch of names to the collection."""
        embeddings = [_normalize(_embed(n)) for n in names]
        ids = [str(uuid.uuid4()) for _ in names]
        self.collection.add(ids=ids, documents=names, embeddings=embeddings)

    def query_embedding(self, text: str, top_k: int, threshold: float) -> list[str]:
        """Query the collection with a piece of text."""
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
            cosine = 1 - dist / 2  # convert L2 (squared) to cosine similarity
            if cosine >= threshold:
                matches.append(doc)
        return matches

    def count(self) -> int:
        """Return the number of items stored in the collection."""
        return self.collection.count()
