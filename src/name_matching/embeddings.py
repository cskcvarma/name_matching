"""Helper functions to get embeddings from OpenAI."""
from __future__ import annotations

import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

_MODEL_NAME = "text-embedding-3-small"
_client: OpenAI | None = None


def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable not set")
    global _client
    if _client is None or _client.api_key != api_key:
        _client = OpenAI(api_key=api_key)
    return _client


def get_embedding(text: str) -> List[float]:
    """Return a single embedding vector for ``text``."""
    client = _get_client()
    response = client.embeddings.create(input=text, model=_MODEL_NAME)
    return response.data[0].embedding


def get_embeddings_batch(texts: List[str]) -> List[List[float]]:
    """Return embedding vectors for ``texts``."""
    client = _get_client()
    response = client.embeddings.create(input=texts, model=_MODEL_NAME)
    return [d.embedding for d in response.data]
