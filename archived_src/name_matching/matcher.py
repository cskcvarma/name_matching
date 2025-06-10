"""Utilities to match names using fuzzy search and embeddings."""

from __future__ import annotations

from collections.abc import Iterable

from rapidfuzz import fuzz, process

from name_matching.db import ChromaDB


class NameMatcher:
    """Find best matches for a query name from a list of existing names."""

    def __init__(
        self,
        existing_names: Iterable[str],
        mode: str = "fuzzy",
        emb_threshold: float = 0.7,
        fuzzy_threshold: float = 0.8,
    ) -> None:
        self.existing_names = list(existing_names)
        self.mode = mode
        self.emb_threshold = emb_threshold
        self.fuzzy_threshold = fuzzy_threshold
        self._db: ChromaDB | None = None
        if mode in {"embedding", "hybrid"}:
            self._db = ChromaDB()
            self._db.add_names_batch(self.existing_names)

    def match_fuzzy(self, query: str, limit: int = 5) -> list[tuple[str, float]]:
        """Return fuzzy matches with their similarity scores."""
        results = process.extract(
            query,
            self.existing_names,
            scorer=fuzz.WRatio,
            score_cutoff=self.fuzzy_threshold * 100,
            limit=limit,
        )
        return [(name, score / 100.0) for name, score, _ in results]

    def match_embedding(self, query: str, limit: int = 5) -> list[str]:
        """Return embedding-based matches for ``query``."""
        if self._db is None:
            self._db = ChromaDB()
            self._db.add_names_batch(self.existing_names)
        return self._db.query_embedding(query, top_k=limit, threshold=self.emb_threshold)

    def find_matches(self, query: str, limit: int = 5) -> list[str]:
        """Return matches using the configured mode."""
        matches: list[str] = []
        if self.mode in {"fuzzy", "hybrid"}:
            matches.extend(name for name, _ in self.match_fuzzy(query, limit))
        if self.mode in {"embedding", "hybrid"}:
            matches.extend(self.match_embedding(query, limit))
        # deduplicate while preserving order
        seen = set()
        unique: list[str] = []
        for name in matches:
            if name not in seen:
                unique.append(name)
                seen.add(name)
        return unique
