import feedparser
import logging
from dataclasses import dataclass
from typing import List
from datetime import datetime

logger = logging.getLogger(__name__)

NEURO_KEYWORDS = [
    "neuroscience", "neurociencia", "dopamine", "dopamina", "psychology",
    "psicología", "psicologia", "brain", "cerebro", "cognitive", "cognitivo",
    "behavior", "comportamiento", "viral", "emotion", "emoción", "habit",
    "hábito", "fear", "miedo", "trust", "confianza", "attention", "atención",
]

RSS_FEEDS = [
    ("https://www.musicbusinessworldwide.com/feed/", "Music Business Worldwide"),
    ("https://www.billboard.com/feed/", "Billboard"),
    ("https://www.marketingweek.com/feed/", "Marketing Week"),
]


@dataclass
class Story:
    title: str
    url: str
    source: str
    summary: str
    published: str
    virality_score: float
    neuroscience_angle: bool


def score_story(story: Story) -> Story:
    text = (story.title + " " + story.summary).lower()
    hits = sum(1 for kw in NEURO_KEYWORDS if kw in text)
    has_neuro = hits > 0
    score = min(1.0, hits * 0.15 + (0.3 if has_neuro else 0))
    return Story(
        title=story.title,
        url=story.url,
        source=story.source,
        summary=story.summary,
        published=story.published,
        virality_score=round(score, 3),
        neuroscience_angle=has_neuro,
    )


class ResearchEngine:
    def _fetch_rss(self, url: str, source: str) -> List[Story]:
        try:
            feed = feedparser.parse(url)
        except Exception as e:
            logger.warning(f"RSS fetch failed for {url}: {e}")
            return []
        stories = []
        for entry in feed.entries[:10]:
            stories.append(
                Story(
                    title=getattr(entry, "title", ""),
                    url=getattr(entry, "link", ""),
                    source=source,
                    summary=getattr(entry, "summary", ""),
                    published=getattr(entry, "published", datetime.now().isoformat()),
                    virality_score=0.0,
                    neuroscience_angle=False,
                )
            )
        return stories

    def fetch_all(self) -> List[Story]:
        all_stories: List[Story] = []
        for url, source in RSS_FEEDS:
            all_stories.extend(self._fetch_rss(url, source))
        return [score_story(s) for s in all_stories]

    def top_stories(self, stories: List[Story], n: int = 5) -> List[Story]:
        return sorted(stories, key=lambda s: s.virality_score, reverse=True)[:n]

    def build_brief(self, story: Story) -> dict:
        neuro_angle = (
            "Ángulo neurociencia/psicología detectado en el texto fuente."
            if story.neuroscience_angle
            else "Requiere ángulo neurociencia manual."
        )
        hook = f"¿Sabías que {story.title.lower().rstrip('.')}?"
        return {
            "titulo_principal": story.title,
            "angulo_neurociencia": neuro_angle,
            "hook_apertura": hook,
            "datos_clave": [story.summary[:200]] if story.summary else [],
            "controversia": "Cuestiona lo establecido — ángulo a definir en escritura.",
            "fuentes": [{"source": story.source, "url": story.url}],
        }

    def run(self) -> dict:
        stories = self.fetch_all()
        if not stories:
            logger.warning("No stories fetched — returning empty brief.")
            return {}
        top = self.top_stories(stories, n=1)
        return self.build_brief(top[0])
