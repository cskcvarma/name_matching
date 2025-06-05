"""Public package exports for name_matching."""

from .db import ChromaDB
from .matcher import NameMatcher

__all__ = ["ChromaDB", "NameMatcher"]
