from unittest.mock import patch, MagicMock
from src.content_engine.research import ResearchEngine, Story, score_story


def test_story_dataclass():
    s = Story(
        title="How dopamine hijacks music purchasing decisions",
        url="https://example.com/story",
        source="Marketing Week",
        summary="New research shows...",
        published="2026-05-28",
        virality_score=0.0,
        neuroscience_angle=True,
    )
    assert s.title == "How dopamine hijacks music purchasing decisions"
    assert s.neuroscience_angle is True


def test_score_story_neuroscience_keywords():
    s = Story(
        title="Dopamine and music consumption: new neuroscience findings",
        url="https://x.com",
        source="Test",
        summary="neurociencia psicología cerebro",
        published="2026-05-28",
        virality_score=0.0,
        neuroscience_angle=False,
    )
    scored = score_story(s)
    assert scored.virality_score > 0
    assert scored.neuroscience_angle is True


def test_score_story_no_neuroscience():
    s = Story(
        title="Quarterly earnings report",
        url="https://x.com",
        source="Test",
        summary="Revenue increased 3%",
        published="2026-05-28",
        virality_score=0.0,
        neuroscience_angle=False,
    )
    scored = score_story(s)
    assert scored.neuroscience_angle is False


def test_engine_produces_brief_structure():
    engine = ResearchEngine()
    mock_story = Story(
        title="Viral hook: how music labels use fear of missing out",
        url="https://mbw.com/story",
        source="Music Business Worldwide",
        summary="Labels exploit psychology. Neurociencia del marketing.",
        published="2026-05-28",
        virality_score=0.8,
        neuroscience_angle=True,
    )
    brief = engine.build_brief(mock_story)
    assert "titulo_principal" in brief
    assert "angulo_neurociencia" in brief
    assert "hook_apertura" in brief
    assert "datos_clave" in brief
    assert "controversia" in brief
    assert "fuentes" in brief
    assert isinstance(brief["datos_clave"], list)
    assert isinstance(brief["fuentes"], list)


def test_engine_rss_parse_mock():
    engine = ResearchEngine()
    mock_feed = MagicMock()
    mock_feed.entries = [
        MagicMock(
            title="Music streaming revenue hits record high",
            link="https://mbw.com/1",
            summary="Streaming revenue. Psychology of listening.",
            published="Wed, 28 May 2026 10:00:00 +0000",
        )
    ]
    with patch("feedparser.parse", return_value=mock_feed):
        stories = engine._fetch_rss("https://fake-url.com", source="MBW")
    assert len(stories) == 1
    assert stories[0].title == "Music streaming revenue hits record high"
    assert stories[0].source == "MBW"


def test_top_stories_sorted_by_score():
    engine = ResearchEngine()
    stories = [
        Story("low", "u", "s", "quarterly report", "2026-05-28", virality_score=0.1, neuroscience_angle=False),
        Story("high", "u", "s", "dopamine neurociencia psicología viral", "2026-05-28", virality_score=0.0, neuroscience_angle=False),
    ]
    scored = [score_story(s) for s in stories]
    top = engine.top_stories(scored, n=1)
    assert top[0].title == "high"
