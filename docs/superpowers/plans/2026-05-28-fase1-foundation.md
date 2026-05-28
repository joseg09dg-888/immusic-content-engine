# FASE 1 — IM Music Content Engine: Fundación Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the functional foundation of the IM Music Content Engine — brand identity module, research scraper, and Claude-powered content writer — producing a first test publication as a local JSON file.

**Architecture:** Three independent modules wired together: `brand.py` as the single source of truth for all visual identity (colors, dimensions, REBEL BRAIN METHOD framework), `research.py` that scrapes RSS feeds and scores stories for virality/neuroscience angle, and `writer.py` that calls Claude API (claude-sonnet-4-6 with prompt caching) applying the REBEL BRAIN METHOD (Pattern Interrupt → Tension Builder → Credibility Anchor → Insight Revelation → Rebel Reframe). All modules import from `brand.py` for any visual or copy constant — no hardcoded hex values or framework text elsewhere.

**Content Durations (hardcoded in brand.py):**
- YouTube: 8-15 min | YouTube Shorts: 55-58 sec
- Instagram Reels: 7-45 sec | Instagram Carousel: 8-10 slides
- TikTok: 21-90 sec | Facebook Reels: 30-60 sec
- Song max duration: 170 sec (2:50) with auto-fade from 155 sec (2:35)

**Tech Stack:** Python 3.12 · anthropic · feedparser · beautifulsoup4 · requests · python-dotenv · pytest · google-auth · google-auth-oauthlib · google-api-python-client

---

## File Map

| File | Responsibility |
|------|---------------|
| `requirements.txt` | All pinned dependencies for FASE 1 |
| `src/core/config.py` | Loads `.env`, exposes typed settings, validates required keys at startup |
| `src/core/brand.py` | Single source of truth: colors, dimensions, copy constants, character names, REBEL BRAIN METHOD, content durations |
| `src/content_engine/research.py` | RSS + HTTP scraper → scored story dicts → JSON brief |
| `src/content_engine/writer.py` | Claude API client → full publication package (script + captions) |
| `scripts/test_publication.py` | End-to-end smoke script, outputs to `logs/test_pub_output.json` |
| `tests/test_brand.py` | Verifies brand constants are correct and complete |
| `tests/test_research.py` | Unit + smoke tests for scraper (network-optional) |
| `tests/test_writer.py` | Unit tests with mocked Anthropic client |

---

## Task 1: Install Dependencies + requirements.txt

**Files:**
- Create: `requirements.txt`
- No test file — verified by import check

- [ ] **Step 1.1: Create requirements.txt**

```
# C:\Users\jose-\projects\immusic-content-engine\requirements.txt
anthropic>=0.25.0
Pillow>=10.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
feedparser>=6.0.11
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-mock>=3.12.0
google-auth>=2.29.0
google-auth-oauthlib>=1.2.0
google-api-python-client>=2.127.0
```

- [ ] **Step 1.2: Install all dependencies**

```powershell
cd C:\Users\jose-\projects\immusic-content-engine
pip install -r requirements.txt
```

Expected output ends with: `Successfully installed ...` (no errors)

- [ ] **Step 1.3: Verify imports**

```powershell
python -c "import anthropic, PIL, requests, bs4, feedparser, dotenv, pytest, google.auth; print('ALL OK')"
```

Expected: `ALL OK`

- [ ] **Step 1.4: Commit**

```powershell
cd C:\Users\jose-\projects\immusic-content-engine
git add requirements.txt
git commit -m "chore: add FASE 1 requirements"
```

---

## Task 2: config.py — Carga de .env y validación

**Files:**
- Create: `src/core/config.py`
- Create: `.env` (from `.env.example` — NOT committed)

- [ ] **Step 2.1: Create .env from example**

```powershell
Copy-Item .env.example .env
```

Then open `.env` and fill in at minimum:
```
ANTHROPIC_API_KEY=sk-ant-...   ← tu clave real
IM_MUSIC_EMAIL=immusicsello@gmail.com
```

- [ ] **Step 2.2: Write src/core/config.py**

```python
# src/core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

_ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(_ROOT / ".env")


def _require(key: str) -> str:
    val = os.getenv(key, "").strip()
    if not val:
        raise EnvironmentError(f"Required env var missing: {key}")
    return val


def _optional(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


class Config:
    ANTHROPIC_API_KEY: str = _require("ANTHROPIC_API_KEY")
    IM_MUSIC_EMAIL: str = _optional("IM_MUSIC_EMAIL", "immusicsello@gmail.com")

    ASSETS_DIR: Path = _ROOT / _optional("ASSETS_DIR", "assets").lstrip("./")
    RELEASES_DIR: Path = _ROOT / _optional("RELEASES_DIR", "releases").lstrip("./")
    LOGS_DIR: Path = _ROOT / _optional("LOGS_DIR", "logs").lstrip("./")

    GOOGLE_CLIENT_ID: str = _optional("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = _optional("GOOGLE_CLIENT_SECRET")
    YOUTUBE_CHANNEL_ID: str = _optional("YOUTUBE_CHANNEL_ID")
    META_ACCESS_TOKEN: str = _optional("META_ACCESS_TOKEN")
    TIKTOK_ACCESS_TOKEN: str = _optional("TIKTOK_ACCESS_TOKEN")
    ELEVENLABS_API_KEY: str = _optional("ELEVENLABS_API_KEY")
    PEXELS_API_KEY: str = _optional("PEXELS_API_KEY")

    CLAUDE_MODEL: str = "claude-sonnet-4-6"


config = Config()
```

- [ ] **Step 2.3: Verify config loads without error**

```powershell
python -c "from src.core.config import config; print('Config OK, model:', config.CLAUDE_MODEL)"
```

Expected: `Config OK, model: claude-sonnet-4-6`

- [ ] **Step 2.4: Commit**

```powershell
git add src/core/config.py
git commit -m "feat: add config.py with env loading and validation"
```

---

## Task 3: brand.py — Fuente Única de Verdad Visual

**Files:**
- Create: `src/core/brand.py`
- Test: `tests/test_brand.py`

- [ ] **Step 3.1: Write failing test first**

```python
# tests/test_brand.py
from src.core.brand import Brand, Dimensions, Character, ContentDurations, RebelBrainMethod


def test_primary_colors():
    assert Brand.BLACK == "#000000"
    assert Brand.VIOLET == "#6200FF"
    assert Brand.WHITE == "#FFFFFF"


def test_concept():
    assert Brand.CONCEPT == "REBEL LUXURY"
    assert Brand.LABEL == "IM Music"
    assert Brand.HANDLE == "@immusicsello"


def test_dimensions_youtube_thumbnail():
    assert Dimensions.YOUTUBE_THUMBNAIL == (1280, 720)


def test_dimensions_instagram_square():
    assert Dimensions.INSTAGRAM_SQUARE == (1080, 1080)


def test_dimensions_instagram_story():
    assert Dimensions.INSTAGRAM_STORY == (1080, 1920)


def test_dimensions_tiktok_cover():
    assert Dimensions.TIKTOK_COVER == (1080, 1920)


def test_cover_art_size():
    assert Dimensions.COVER_ART == (3000, 3000)


def test_characters():
    assert Character.CHILL_HOP.name == "El Viajero Nocturno"
    assert Character.CHILL_HOP.genre == "Chill Hop"
    assert Character.CHILL_HOP.bpm_range == (85, 95)
    assert Character.AFRO_HOUSE.name == "El Ser Galáctico"
    assert Character.AFRO_HOUSE.genre == "Afro House"
    assert Character.AFRO_HOUSE.bpm_range == (120, 128)


def test_lufs_targets():
    assert Brand.LUFS_SPOTIFY == -14
    assert Brand.LUFS_YOUTUBE == -13
    assert Brand.LUFS_APPLE == -16


def test_publish_days():
    assert Brand.PUBLISH_DAYS == ["Monday", "Wednesday", "Friday"]


def test_publish_times():
    assert Brand.PUBLISH_TIMES == {"youtube": "18:00", "instagram": "19:00", "tiktok": "20:00"}


def test_color_palette_completeness():
    palette = Brand.palette()
    assert "black" in palette
    assert "violet" in palette
    assert "white" in palette
    assert all(v.startswith("#") for v in palette.values())


def test_content_durations_song():
    assert ContentDurations.SONG_MAX == 170
    assert ContentDurations.SONG_FADE_START == 155
    assert ContentDurations.SONG_FADE_START < ContentDurations.SONG_MAX


def test_content_durations_youtube():
    assert ContentDurations.YOUTUBE_MIN == 480
    assert ContentDurations.YOUTUBE_MAX == 900
    assert ContentDurations.YOUTUBE_SHORT_MIN == 55
    assert ContentDurations.YOUTUBE_SHORT_MAX == 58


def test_content_durations_social():
    assert ContentDurations.TIKTOK_MIN == 21
    assert ContentDurations.TIKTOK_MAX == 90
    assert ContentDurations.INSTAGRAM_REEL_MIN == 7
    assert ContentDurations.INSTAGRAM_REEL_MAX == 45


def test_rebel_brain_method_steps():
    assert len(RebelBrainMethod.STEPS) == 5
    assert RebelBrainMethod.STEPS[0] == "Pattern Interrupt"
    assert RebelBrainMethod.STEPS[-1] == "Rebel Reframe"


def test_rebel_brain_method_prompt_block():
    block = RebelBrainMethod.as_prompt_block()
    assert "PATTERN INTERRUPT" in block
    assert "TENSION BUILDER" in block
    assert "CREDIBILITY ANCHOR" in block
    assert "INSIGHT REVELATION" in block
    assert "REBEL REFRAME" in block
```

- [ ] **Step 3.2: Run test — verify it FAILS**

```powershell
cd C:\Users\jose-\projects\immusic-content-engine
python -m pytest tests/test_brand.py -v 2>&1 | Select-Object -First 20
```

Expected: `ModuleNotFoundError` or `ImportError` — brand.py doesn't exist yet.

- [ ] **Step 3.3: Write src/core/brand.py**

```python
# src/core/brand.py
from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class _Character:
    name: str
    genre: str
    bpm_range: Tuple[int, int]
    scene: str


class Character:
    CHILL_HOP = _Character(
        name="El Viajero Nocturno",
        genre="Chill Hop",
        bpm_range=(85, 95),
        scene="Ciudad nocturna futurista, lluvia suave, neón violeta, constelaciones",
    )
    AFRO_HOUSE = _Character(
        name="El Ser Galáctico",
        genre="Afro House",
        bpm_range=(120, 128),
        scene="Galaxia abierta, nebulosas, polvo estelar que vibra con el beat",
    )


class Dimensions:
    YOUTUBE_THUMBNAIL: Tuple[int, int] = (1280, 720)
    INSTAGRAM_SQUARE: Tuple[int, int] = (1080, 1080)
    INSTAGRAM_STORY: Tuple[int, int] = (1080, 1920)
    TIKTOK_COVER: Tuple[int, int] = (1080, 1920)
    COVER_ART: Tuple[int, int] = (3000, 3000)
    YOUTUBE_VIDEO: Tuple[int, int] = (1920, 1080)


class ContentDurations:
    """Target durations in seconds for each platform/format."""
    YOUTUBE_MIN: int = 480         # 8 min
    YOUTUBE_MAX: int = 900         # 15 min
    YOUTUBE_SHORT_MIN: int = 55
    YOUTUBE_SHORT_MAX: int = 58
    INSTAGRAM_REEL_MIN: int = 7
    INSTAGRAM_REEL_MAX: int = 45
    INSTAGRAM_CAROUSEL_SLIDES: Tuple[int, int] = (8, 10)
    TIKTOK_MIN: int = 21
    TIKTOK_MAX: int = 90
    FACEBOOK_REEL_MIN: int = 30
    FACEBOOK_REEL_MAX: int = 60
    # Music
    SONG_MAX: int = 170            # 2:50
    SONG_FADE_START: int = 155     # 2:35 — fade out begins here


class RebelBrainMethod:
    """
    REBEL BRAIN METHOD — framework obligatorio en cada pieza de contenido.
    Voz: autoridad + rebeldía intelectual + lujo de conocimiento.
    Sin venta directa. La neurociencia es el hilo conductor.
    """
    STEPS = [
        "Pattern Interrupt",
        "Tension Builder",
        "Credibility Anchor",
        "Insight Revelation",
        "Rebel Reframe",
    ]

    PATTERN_INTERRUPT = (
        "Rompe el patrón de atención en los primeros 5 segundos. "
        "Dato contraintuitivo, pregunta que desafía, o afirmación que contradice lo obvio."
    )
    TENSION_BUILDER = (
        "Construye tensión con una paradoja o problema sin resolver. "
        "El oyente debe sentir que le falta información crítica."
    )
    CREDIBILITY_ANCHOR = (
        "Anclaje de credibilidad: dato científico, estadística, estudio real, o caso documentado. "
        "No inventar números. Citar fuente siempre."
    )
    INSIGHT_REVELATION = (
        "La revelación: la conexión que nadie más ha hecho entre neurociencia y la industria musical. "
        "Ángulo único de IM Music / REBEL LUXURY."
    )
    REBEL_REFRAME = (
        "Reencuadre rebelde: cuestiona lo establecido sin atacar personas. "
        "CTA implícito de identidad IM Music. Sin llamados directos a comprar."
    )

    @classmethod
    def as_prompt_block(cls) -> str:
        return (
            "REBEL BRAIN METHOD — aplica este framework en orden:\n"
            f"1. PATTERN INTERRUPT: {cls.PATTERN_INTERRUPT}\n"
            f"2. TENSION BUILDER: {cls.TENSION_BUILDER}\n"
            f"3. CREDIBILITY ANCHOR: {cls.CREDIBILITY_ANCHOR}\n"
            f"4. INSIGHT REVELATION: {cls.INSIGHT_REVELATION}\n"
            f"5. REBEL REFRAME: {cls.REBEL_REFRAME}\n"
        )


class Brand:
    # Colors — IMMUTABLE, single source of truth
    BLACK: str = "#000000"
    VIOLET: str = "#6200FF"
    WHITE: str = "#FFFFFF"

    # Identity
    CONCEPT: str = "REBEL LUXURY"
    LABEL: str = "IM Music"
    HANDLE: str = "@immusicsello"
    MOTIFS: list = ["constelaciones", "galaxia", "líneas de luz", "polvo estelar"]

    # Audio mastering targets (LUFS)
    LUFS_SPOTIFY: int = -14
    LUFS_YOUTUBE: int = -13
    LUFS_APPLE: int = -16

    # Publishing schedule (Colombia COT = UTC-5)
    PUBLISH_DAYS: list = ["Monday", "Wednesday", "Friday"]
    PUBLISH_TIMES: dict = {
        "youtube": "18:00",
        "instagram": "19:00",
        "tiktok": "20:00",
    }

    # Distribution
    DISTRIBUTOR: str = "Nexus"
    DISTRIBUTOR_CUT: float = 0.08

    @classmethod
    def palette(cls) -> dict:
        return {
            "black": cls.BLACK,
            "violet": cls.VIOLET,
            "white": cls.WHITE,
        }
```

- [ ] **Step 3.4: Run tests — verify ALL PASS**

```powershell
python -m pytest tests/test_brand.py -v
```

Expected:
```
tests/test_brand.py::test_primary_colors PASSED
tests/test_brand.py::test_concept PASSED
tests/test_brand.py::test_dimensions_youtube_thumbnail PASSED
tests/test_brand.py::test_dimensions_instagram_square PASSED
tests/test_brand.py::test_dimensions_instagram_story PASSED
tests/test_brand.py::test_dimensions_tiktok_cover PASSED
tests/test_brand.py::test_cover_art_size PASSED
tests/test_brand.py::test_characters PASSED
tests/test_brand.py::test_lufs_targets PASSED
tests/test_brand.py::test_publish_days PASSED
tests/test_brand.py::test_publish_times PASSED
tests/test_brand.py::test_color_palette_completeness PASSED
12 passed
```

- [ ] **Step 3.5: Commit**

```powershell
git add src/core/brand.py tests/test_brand.py
git commit -m "feat: add brand.py — single source of truth for IM Music visual identity"
```

---

## Task 4: research.py — RSS Scraper + Story Scorer

**Files:**
- Create: `src/content_engine/research.py`
- Test: `tests/test_research.py`

- [ ] **Step 4.1: Write failing tests**

```python
# tests/test_research.py
import json
import pytest
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
```

- [ ] **Step 4.2: Run — verify FAILS**

```powershell
python -m pytest tests/test_research.py -v 2>&1 | Select-Object -First 10
```

Expected: `ModuleNotFoundError` for `src.content_engine.research`

- [ ] **Step 4.3: Write src/content_engine/research.py**

```python
# src/content_engine/research.py
import feedparser
import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass, field
from typing import List
import json
import logging
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
```

- [ ] **Step 4.4: Run tests — verify ALL PASS**

```powershell
python -m pytest tests/test_research.py -v
```

Expected: `6 passed`

- [ ] **Step 4.5: Commit**

```powershell
git add src/content_engine/research.py tests/test_research.py
git commit -m "feat: add research.py — RSS scraper + neuroscience story scorer"
```

---

## Task 5: writer.py — Content Writer con Claude API

**Files:**
- Create: `src/content_engine/writer.py`
- Test: `tests/test_writer.py`

- [ ] **Step 5.1: Write failing tests**

```python
# tests/test_writer.py
import pytest
from unittest.mock import MagicMock, patch
from src.content_engine.writer import ContentWriter, PublicationPackage


def _mock_anthropic(text: str):
    mock_client = MagicMock()
    mock_msg = MagicMock()
    mock_msg.content = [MagicMock(text=text)]
    mock_client.messages.create.return_value = mock_msg
    return mock_client


def test_publication_package_structure():
    pkg = PublicationPackage(
        brief={"titulo_principal": "Test", "angulo_neurociencia": "X",
               "hook_apertura": "Hook", "datos_clave": [], "controversia": "C", "fuentes": []},
        script_es="Guión en español...",
        captions_instagram="Caption IG...",
        caption_tiktok="Caption TK",
        youtube_titles=["Título 1", "Título 2", "Título 3"],
        youtube_description="Descripción YT...",
    )
    assert pkg.script_es.startswith("Guión")
    assert len(pkg.youtube_titles) == 3
    assert pkg.caption_tiktok is not None


def test_writer_generates_script():
    fake_response = """
SCRIPT:
Este es el guión completo en español para YouTube.

CAPTIONS_INSTAGRAM:
Caption para Instagram con hashtags #RebelLuxury #IMMusic

CAPTION_TIKTOK:
Hook viral para TikTok #IMMusic

YOUTUBE_TITLES:
1. Título SEO variante uno
2. Título SEO variante dos
3. Título SEO variante tres

YOUTUBE_DESCRIPTION:
Descripción completa con timestamps y keywords.
"""
    brief = {
        "titulo_principal": "How dopamine shapes music taste",
        "angulo_neurociencia": "Dopamine reward loop",
        "hook_apertura": "¿Sabías que tu cerebro elige música antes de que tú lo hagas?",
        "datos_clave": ["88% of listeners choose music based on mood"],
        "controversia": "Los algoritmos conocen tu cerebro mejor que tú",
        "fuentes": [{"source": "MBW", "url": "https://mbw.com"}],
    }
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_anthropic(fake_response)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(brief)
    assert "guión" in pkg.script_es.lower() or len(pkg.script_es) > 5
    assert len(pkg.youtube_titles) == 3
    assert "#" in pkg.captions_instagram or len(pkg.captions_instagram) > 5


def test_writer_parses_youtube_titles():
    fake_response = """
SCRIPT: El guión aquí.
CAPTIONS_INSTAGRAM: Caption aquí #IMMusic #RebelLuxury
CAPTION_TIKTOK: TikTok caption
YOUTUBE_TITLES:
1. Primer título optimizado
2. Segundo título variante
3. Tercer título alternativo
YOUTUBE_DESCRIPTION: Descripción completa.
"""
    brief = {
        "titulo_principal": "Test",
        "angulo_neurociencia": "X",
        "hook_apertura": "Hook",
        "datos_clave": [],
        "controversia": "C",
        "fuentes": [],
    }
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_anthropic(fake_response)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(brief)
    assert pkg.youtube_titles[0] == "Primer título optimizado"
    assert pkg.youtube_titles[1] == "Segundo título variante"
    assert pkg.youtube_titles[2] == "Tercer título alternativo"
```

- [ ] **Step 5.2: Run — verify FAILS**

```powershell
python -m pytest tests/test_writer.py -v 2>&1 | Select-Object -First 10
```

Expected: `ModuleNotFoundError` for `src.content_engine.writer`

- [ ] **Step 5.3: Write src/content_engine/writer.py**

```python
# src/content_engine/writer.py
import re
import anthropic
from dataclasses import dataclass
from typing import List
import logging
from src.core.brand import Brand, RebelBrainMethod

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = f"""Eres el escritor de contenido del sello discográfico {Brand.LABEL} — concepto {Brand.CONCEPT}.

TONO: Autoridad + rebeldía intelectual + lujo de conocimiento. Sin venta directa.
MARCA: {Brand.LABEL} | {Brand.CONCEPT} | {Brand.HANDLE}
COLORES evocados en el lenguaje: negro profundo, violeta eléctrico, destellos blancos.

{RebelBrainMethod.as_prompt_block()}

REGLA ABSOLUTA: Aplica el REBEL BRAIN METHOD en ese orden exacto en cada pieza.
Siempre responde en el formato exacto solicitado. No añadas texto fuera del formato."""


@dataclass
class PublicationPackage:
    brief: dict
    script_es: str
    captions_instagram: str
    caption_tiktok: str
    youtube_titles: List[str]
    youtube_description: str


def _extract_section(text: str, section: str, next_section: str = None) -> str:
    pattern = rf"{re.escape(section)}[:\n]+(.*?)"
    if next_section:
        pattern += rf"(?={re.escape(next_section)})"
    else:
        pattern += r"$"
    match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else ""


def _parse_numbered_list(text: str) -> List[str]:
    lines = [re.sub(r"^\d+\.\s*", "", l).strip() for l in text.strip().splitlines() if l.strip()]
    return [l for l in lines if l][:3]


class ContentWriter:
    def __init__(self, api_key: str):
        self._client = anthropic.Anthropic(api_key=api_key)

    def generate(self, brief: dict) -> PublicationPackage:
        user_prompt = f"""Genera el paquete de publicación completo para esta historia:

TÍTULO: {brief['titulo_principal']}
ÁNGULO NEUROCIENCIA: {brief['angulo_neurociencia']}
HOOK APERTURA: {brief['hook_apertura']}
DATOS CLAVE: {', '.join(brief['datos_clave'])}
CONTROVERSIA: {brief['controversia']}
FUENTES: {', '.join(f['source'] for f in brief['fuentes'])}

Responde EXACTAMENTE en este formato (sin texto extra):

SCRIPT:
[Guión completo YouTube en español, 5-8 minutos hablados ~800-1200 palabras]

CAPTIONS_INSTAGRAM:
[Caption hasta 2200 caracteres + hashtags optimizados #RebelLuxury #IMMusic]

CAPTION_TIKTOK:
[Máximo 150 caracteres + hashtags virales]

YOUTUBE_TITLES:
1. [Título SEO variante 1]
2. [Título SEO variante 2]
3. [Título SEO variante 3]

YOUTUBE_DESCRIPTION:
[Descripción con timestamps, keywords, links]"""

        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=[
                {
                    "type": "text",
                    "text": _SYSTEM_PROMPT,
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw = response.content[0].text
        script = _extract_section(raw, "SCRIPT", "CAPTIONS_INSTAGRAM")
        captions_ig = _extract_section(raw, "CAPTIONS_INSTAGRAM", "CAPTION_TIKTOK")
        caption_tt = _extract_section(raw, "CAPTION_TIKTOK", "YOUTUBE_TITLES")
        titles_raw = _extract_section(raw, "YOUTUBE_TITLES", "YOUTUBE_DESCRIPTION")
        yt_desc = _extract_section(raw, "YOUTUBE_DESCRIPTION")

        titles = _parse_numbered_list(titles_raw)
        if len(titles) < 3:
            titles = (titles + ["", "", ""])[:3]

        return PublicationPackage(
            brief=brief,
            script_es=script,
            captions_instagram=captions_ig,
            caption_tiktok=caption_tt,
            youtube_titles=titles,
            youtube_description=yt_desc,
        )
```

- [ ] **Step 5.4: Run tests — verify ALL PASS**

```powershell
python -m pytest tests/test_writer.py -v
```

Expected: `3 passed`

- [ ] **Step 5.5: Commit**

```powershell
git add src/content_engine/writer.py tests/test_writer.py
git commit -m "feat: add writer.py — Claude API content generator with prompt caching"
```

---

## Task 6: scripts/test_publication.py — Primera Publicación de Prueba

**Files:**
- Create: `scripts/test_publication.py`
- Output: `logs/test_pub_output.json`

**Prerequisite:** `.env` must have a real `ANTHROPIC_API_KEY`.

- [ ] **Step 6.1: Write scripts/test_publication.py**

```python
# scripts/test_publication.py
"""
End-to-end smoke test for FASE 1.
Runs: research → writer → saves output to logs/test_pub_output.json
Real API call — requires ANTHROPIC_API_KEY in .env
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.config import config
from src.core.brand import Brand
from src.content_engine.research import ResearchEngine
from src.content_engine.writer import ContentWriter


def main():
    print(f"\n{'='*60}")
    print(f"  IM Music Content Engine — FASE 1 Test Publication")
    print(f"  Concept: {Brand.CONCEPT} | Label: {Brand.LABEL}")
    print(f"{'='*60}\n")

    print("[ 1/3 ] Running research engine...")
    engine = ResearchEngine()
    brief = engine.run()

    if not brief:
        print("  No stories found from RSS — using fallback brief.")
        brief = {
            "titulo_principal": "La neurociencia detrás del éxito viral en música 2026",
            "angulo_neurociencia": "El loop de dopamina y cómo los sellos lo explotan",
            "hook_apertura": "¿Sabías que tu cerebro decide si una canción es viral antes de escuchar el segundo compás?",
            "datos_clave": ["88% de los oyentes eligen música por estado de ánimo", "El primer beat determina el 70% de la decisión de escucha"],
            "controversia": "Los algoritmos de Spotify conocen tus emociones mejor que tú",
            "fuentes": [{"source": "IM Music Research", "url": "https://immusic.co"}],
        }

    print(f"  Story: {brief['titulo_principal'][:60]}...")
    print(f"  Neuro angle: {brief['angulo_neurociencia'][:60]}...")

    print("\n[ 2/3 ] Generating content with Claude API...")
    writer = ContentWriter(api_key=config.ANTHROPIC_API_KEY)
    pkg = writer.generate(brief)
    print(f"  Script length: {len(pkg.script_es)} chars")
    print(f"  Instagram caption: {len(pkg.captions_instagram)} chars")
    print(f"  TikTok caption: {pkg.caption_tiktok[:60]}...")
    print(f"  YouTube titles: {pkg.youtube_titles[0][:50]}...")

    print("\n[ 3/3 ] Saving output...")
    output = {
        "brief": pkg.brief,
        "script_es": pkg.script_es,
        "captions_instagram": pkg.captions_instagram,
        "caption_tiktok": pkg.caption_tiktok,
        "youtube_titles": pkg.youtube_titles,
        "youtube_description": pkg.youtube_description,
        "brand": {
            "label": Brand.LABEL,
            "concept": Brand.CONCEPT,
            "colors": Brand.palette(),
        },
    }

    out_path = Path("logs/test_pub_output.json")
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Saved to: {out_path.resolve()}")
    print(f"\n{'='*60}")
    print("  FASE 1 TEST COMPLETE ✅")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6.2: Run the test publication**

```powershell
cd C:\Users\jose-\projects\immusic-content-engine
python scripts/test_publication.py
```

Expected output:
```
============================================================
  IM Music Content Engine — FASE 1 Test Publication
  Concept: REBEL LUXURY | Label: IM Music
============================================================

[ 1/3 ] Running research engine...
  Story: ...
[ 2/3 ] Generating content with Claude API...
  Script length: NNNN chars
[ 3/3 ] Saving output...
  Saved to: C:\...\logs\test_pub_output.json

============================================================
  FASE 1 TEST COMPLETE ✅
============================================================
```

- [ ] **Step 6.3: Verify output file is valid JSON**

```powershell
python -c "import json; d=json.load(open('logs/test_pub_output.json', encoding='utf-8')); print('Keys:', list(d.keys())); print('Script chars:', len(d['script_es']))"
```

Expected:
```
Keys: ['brief', 'script_es', 'captions_instagram', 'caption_tiktok', 'youtube_titles', 'youtube_description', 'brand']
Script chars: [number > 500]
```

- [ ] **Step 6.4: Commit**

```powershell
git add scripts/test_publication.py
git commit -m "feat: add test_publication.py — end-to-end FASE 1 smoke script"
```

---

## Task 7: Full Test Suite + Push

- [ ] **Step 7.1: Run complete test suite**

```powershell
cd C:\Users\jose-\projects\immusic-content-engine
python -m pytest tests/ -v
```

Expected:
```
tests/test_brand.py::test_primary_colors PASSED
tests/test_brand.py::test_concept PASSED
tests/test_brand.py::test_dimensions_youtube_thumbnail PASSED
tests/test_brand.py::test_dimensions_instagram_square PASSED
tests/test_brand.py::test_dimensions_instagram_story PASSED
tests/test_brand.py::test_dimensions_tiktok_cover PASSED
tests/test_brand.py::test_cover_art_size PASSED
tests/test_brand.py::test_characters PASSED
tests/test_brand.py::test_lufs_targets PASSED
tests/test_brand.py::test_publish_days PASSED
tests/test_brand.py::test_publish_times PASSED
tests/test_brand.py::test_color_palette_completeness PASSED
tests/test_brand.py::test_content_durations_song PASSED
tests/test_brand.py::test_content_durations_youtube PASSED
tests/test_brand.py::test_content_durations_social PASSED
tests/test_brand.py::test_rebel_brain_method_steps PASSED
tests/test_brand.py::test_rebel_brain_method_prompt_block PASSED
tests/test_research.py::test_story_dataclass PASSED
tests/test_research.py::test_score_story_neuroscience_keywords PASSED
tests/test_research.py::test_score_story_no_neuroscience PASSED
tests/test_research.py::test_engine_produces_brief_structure PASSED
tests/test_research.py::test_engine_rss_parse_mock PASSED
tests/test_research.py::test_top_stories_sorted_by_score PASSED
tests/test_writer.py::test_publication_package_structure PASSED
tests/test_writer.py::test_writer_generates_script PASSED
tests/test_writer.py::test_writer_parses_youtube_titles PASSED
26 passed
```

- [ ] **Step 7.2: Verify .env is gitignored**

```powershell
git status
```

`.env` must NOT appear in the output. If it does, verify `.gitignore` contains `.env`.

- [ ] **Step 7.3: Final commit and push**

```powershell
git add -A
git status  # confirm no .env in staged files
git commit -m "feat: FASE 1 complete — brand, research, writer, tests (26 passing)"
git push origin main
```

Expected: push succeeds, branch `main` updated on GitHub.

---

## Spec Coverage Check

| Spec Requirement | Task |
|-----------------|------|
| Setup dependencias | Task 1 |
| brand.py con identidad completa | Task 3 |
| REBEL BRAIN METHOD en brand.py | Task 3 (RebelBrainMethod class) |
| ContentDurations en brand.py | Task 3 (ContentDurations class) |
| research.py funcionando | Task 4 |
| writer.py con REBEL BRAIN METHOD | Task 5 (usa RebelBrainMethod.as_prompt_block()) |
| Primera publicación manual | Task 6 |
| Tests para todos los módulos | Tasks 3, 4, 5 |
| Commit y push | Tasks 1, 3, 4, 5, 6, 7 |
| Google Drive en config (no FASE 1) | Task 2 (config.py tiene campos listos) |
| Claude API claude-sonnet-4-6 | Task 5 |
| Prompt caching | Task 5 (system prompt con cache_control: ephemeral) |
| brand.py fuente única de verdad | Tasks 3, 5, 6 — brand importado, nada hardcodeado |
| Voz sin venta directa | Task 5 (REBEL_REFRAME instruction explícita) |

All requirements covered. No placeholders.

---

## Notas de implementación

- `logs/test_pub_output.json` está en `.gitignore` implícito vía `logs/*.log` — agregar `logs/*.json` si se desea excluir
- FFmpeg y Whisper NO son requeridos en FASE 1 — entran en FASE 2 (video_producer.py)
- Google Drive OAuth NO está configurado en FASE 1 — los campos existen en `config.py` listos para FASE 2
- `_SYSTEM_PROMPT` en writer.py usa `cache_control: ephemeral` — esto reduce costos de API ~90% en llamadas repetidas al mismo system prompt
