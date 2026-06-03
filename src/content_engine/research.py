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
    # Industria musical
    ("https://www.musicbusinessworldwide.com/feed/", "Music Business Worldwide"),
    ("https://www.billboard.com/feed/", "Billboard"),
    ("https://variety.com/v/music/feed/", "Variety Music"),
    ("https://www.rollingstone.com/music/feed/", "Rolling Stone"),
    # Marketing y negocios
    ("https://www.marketingweek.com/feed/", "Marketing Week"),
    ("https://adage.com/rss/all", "Ad Age"),
    # Reddit (JSON feeds)
    ("https://www.reddit.com/r/musicbusiness/.rss", "Reddit r/musicbusiness"),
    ("https://www.reddit.com/r/WeAreTheMusicMakers/.rss", "Reddit r/WeAreTheMusicMakers"),
    ("https://www.reddit.com/r/marketing/.rss", "Reddit r/marketing"),
    # Streaming/tech música
    ("https://musically.com/feed/", "Music Ally"),
    ("https://podnews.net/rss", "Podnews"),
]

# Temáticas obligatorias para filtrado
TOPIC_KEYWORDS = [
    # Marketing musical
    "marketing", "viral", "campaign", "strategy", "brand", "audience",
    # Plataformas
    "tiktok", "spotify", "youtube", "instagram", "streaming", "playlist",
    "soundon", "distrokid", "tunecore", "distribution",
    # Industria
    "label", "sello", "artist", "artista", "release", "lanzamiento",
    "album", "single", "chart", "billboard", "streams",
    # Neurociencia/psicología
    "neuroscience", "neurociencia", "psychology", "psicologia", "emotion",
    "behavior", "viral", "attention", "hook", "dopamine",
    # Casos reales
    "independent", "independiente", "deal", "deal", "rights", "publishing",
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
    neuro_hits = sum(1 for kw in NEURO_KEYWORDS if kw in text)
    topic_hits = sum(1 for kw in TOPIC_KEYWORDS if kw in text)
    has_neuro = neuro_hits > 0
    # Score: neuro keywords (alta prioridad) + topic keywords + penalizar si no hay nada relevante
    score = min(1.0,
        neuro_hits * 0.15 +
        topic_hits * 0.06 +
        (0.25 if has_neuro else 0) +
        (0.1 if "tiktok" in text or "spotify" in text or "youtube" in text else 0) +
        (0.1 if "viral" in text else 0)
    )
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

    @staticmethod
    def _clean_text(text: str) -> str:
        """Elimina HTML tags y caracteres especiales de texto RSS."""
        import re, html
        text = html.unescape(text)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def build_brief(self, story: Story) -> dict:
        neuro_angle = (
            "Ángulo neurociencia/psicología: hay datos de comportamiento, atención o emoción en la historia."
            if story.neuroscience_angle
            else "Requiere ángulo neurociencia: aplicar psicología del consumidor o sesgo cognitivo."
        )
        # Hook tipo Rebel Brain Method — Pattern Interrupt
        title_lower = story.title.lower().rstrip(".")
        hook = f"Lo que {story.source} acaba de revelar cambia todo lo que creías saber."
        clean_summary = self._clean_text(story.summary)[:300] if story.summary else ""
        clean_title   = self._clean_text(story.title)

        return {
            "titulo_principal": clean_title,
            "angulo_neurociencia": neuro_angle,
            "hook_apertura": hook,
            "datos_clave": [clean_summary] if clean_summary else [],
            "controversia": f"La industria lleva tiempo sabiendo esto. La pregunta es: ¿por qué no te lo dijeron antes?",
            "fuentes": [{"source": story.source, "url": story.url}],
            "audiencia": "Artistas independientes 17-35 años, Medellín y Latinoamérica",
            "formato": "carousel",
            "plataforma": "instagram",
            "tema_categoria": _classify_topic(story.title + " " + story.summary),
        }

def _classify_topic(text: str) -> str:
    text = text.lower()
    if any(k in text for k in ["tiktok", "viral", "trend"]):
        return "TikTok y viralidad"
    if any(k in text for k in ["spotify", "streaming", "playlist", "streams"]):
        return "Distribución y streaming"
    if any(k in text for k in ["youtube", "shorts", "monetiz"]):
        return "YouTube y monetización"
    if any(k in text for k in ["marketing", "campaign", "brand", "strategy"]):
        return "Marketing musical"
    if any(k in text for k in ["neuroscience", "psychology", "behavior", "emotion"]):
        return "Neurociencia y psicología"
    if any(k in text for k in ["artist", "artista", "release", "label", "sello"]):
        return "Desarrollo de artistas"
    return "Industria musical"

    def run(self) -> dict:
        stories = self.fetch_all()
        if not stories:
            logger.warning("No stories fetched — returning empty brief.")
            return {}
        top = self.top_stories(stories, n=1)
        return self.build_brief(top[0])
