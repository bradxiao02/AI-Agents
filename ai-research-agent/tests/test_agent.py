
from src.agent import conduct_research


def test_empty_query():
    try:
        conduct_research("")
        assert False, "Expected ValueError"
    except ValueError:
        assert True


def test_no_search_results(monkeypatch):
    monkeypatch.setattr(
        "src.agent.search_web",
        lambda query, max_results=5: []
    )

    result = conduct_research("Digital forensics")

    assert result["success"] is False
    assert result["sources"] == []


def test_successful_research(monkeypatch):
    fake_sources = [
        {
            "title": "Test Source",
            "url": "https://example.com",
            "snippet": "Artificial intelligence in forensics."
        }
    ]

    monkeypatch.setattr(
        "src.agent.search_web",
        lambda query, max_results=5: fake_sources
    )

    monkeypatch.setattr(
    "src.agent.analyze_research",
    lambda query, sources, mode="General": "Test research report"
    )

    monkeypatch.setattr(
        "src.agent.save_research",
        lambda topic, report: None
    )

    result = conduct_research("AI in digital forensics")

    assert result["success"] is True
    assert result["report"].startswith("Test research report")
    assert "## References" in result["report"]
    assert "[1]" in result["report"]
    assert "https://example.com" in result["report"]
    assert len(result["sources"]) == 1
