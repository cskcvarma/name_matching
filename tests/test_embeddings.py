import importlib
import os
import pytest

from name_matching import embeddings


@pytest.mark.skipif("OPENAI_API_KEY" not in os.environ, reason="OPENAI_API_KEY not set")
def test_get_embedding_shape():
    vec = embeddings.get_embedding("test")
    assert isinstance(vec, list)
    assert len(vec) == 1536
    assert all(isinstance(x, float) for x in vec)


def test_bad_api_key(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "bad-key")
    importlib.reload(embeddings)  # reload to pick up new key
    with pytest.raises(Exception):
        embeddings.get_embedding("test")
