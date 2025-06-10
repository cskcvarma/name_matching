from name_matching import matcher


def test_match_fuzzy_basic():
    m = matcher.NameMatcher(["John Doe", "Jane Doe"], mode="fuzzy", fuzzy_threshold=0.8)
    results = m.match_fuzzy("Jon Doe")
    assert results
    name, score = results[0]
    assert name == "John Doe"
    assert score >= 0.8


def test_match_embedding_stub(monkeypatch):
    class DummyDB:
        def __init__(self) -> None:
            pass

        def add_names_batch(self, names: list[str]) -> None:
            self.names = names

        def query_embedding(self, text: str, top_k: int, threshold: float) -> list[str]:
            _ = top_k, threshold
            assert text == "John"
            return ["John Doe"]

    monkeypatch.setattr(matcher, "ChromaDB", DummyDB)
    m = matcher.NameMatcher(["John Doe"], mode="embedding")
    results = m.match_embedding("John")
    assert results == ["John Doe"]


def test_hybrid_mode(monkeypatch):
    class DummyDB:
        def __init__(self) -> None:
            pass

        def add_names_batch(self, names: list[str]) -> None:
            self.names = names

        def query_embedding(self, text: str, top_k: int, threshold: float) -> list[str]:
            _ = text, top_k, threshold
            return ["Alice"]

    monkeypatch.setattr(matcher, "ChromaDB", DummyDB)
    names = ["John Doe", "Alice"]
    m = matcher.NameMatcher(names, mode="hybrid", fuzzy_threshold=0.8)
    matches = m.find_matches("Jon Doe")
    assert "John Doe" in matches
    assert "Alice" in matches
