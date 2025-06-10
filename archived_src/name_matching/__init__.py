"""Public package exports for name_matching."""

from .db import ChromaDB
from .loader import load_fake_names
from .matcher import NameMatcher

__all__ = ["ChromaDB", "NameMatcher", "load_fake_names"]
