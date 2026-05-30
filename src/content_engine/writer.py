import re
import anthropic
from dataclasses import dataclass, field
from typing import List, Optional
import logging
from src.core.brand import Brand, RebelBrainMethod, VoiceProfile

logger = logging.getLogger(__name__)

_SYSTEM_PROMPT = f"""Eres el escritor de contenido de {Brand.LABEL} — sello discográfico basado en Medellín, Colombia.

{VoiceProfile.as_prompt_block()}

{RebelBrainMethod.as_prompt_block()}

REGLAS ABSOLUTAS DE VOZ:
- Mezcla lenguaje urbano con terminología técnica — suenas a la calle Y a la sala de juntas
- Todo el mundo te entiende aunque seas muy técnico — si algo suena académico, simplifícalo sin perder profundidad
- NUNCA genérico — si una frase la podría escribir cualquier otra marca, reescríbela
- No compites con nadie — eres el único que hace esto así y punto
- Incomodas cuando toca — sin pedir permiso ni disculpas, pero siempre con respeto
- La psicología es el hilo conductor: neurociencia, comportamiento, sesgo cognitivo aplicado a la música
- Cada pieza aplica REBEL BRAIN METHOD en orden: Pattern Interrupt → Tension Builder → Credibility Anchor → Insight Revelation → Rebel Reframe

FORMATO: Responde EXACTAMENTE con las secciones indicadas. Sin texto fuera del formato."""


@dataclass
class CarouselSlide:
    number: int
    title: str
    body: str


@dataclass
class PublicationPackage:
    brief: dict
    # Scripts por plataforma
    script_es: str                              # YouTube completo 8-15 min
    script_short: str = ""                      # YouTube Shorts 55-58 seg
    script_instagram_reel: str = ""             # IG Reel 7-45 seg
    script_tiktok: str = ""                     # TikTok 21-90 seg
    script_facebook_reel: str = ""              # FB Reel 30-60 seg
    # Carrusel
    carousel_slides: List[CarouselSlide] = field(default_factory=list)
    # Captions
    captions_instagram: str = ""
    caption_tiktok: str = ""
    caption_facebook: str = ""
    caption_youtube: str = ""
    # SEO YouTube
    youtube_titles: List[str] = field(default_factory=list)
    youtube_description: str = ""


def _section(text: str, start: str, end: str = None) -> str:
    pattern = rf"{re.escape(start)}[:\n]+(.*?)"
    pattern += rf"(?={re.escape(end)})" if end else r"$"
    m = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
    return m.group(1).strip() if m else ""


def _numbered_lines(text: str, n: int = 3) -> List[str]:
    lines = [re.sub(r"^\d+[\.\)]\s*", "", l).strip() for l in text.strip().splitlines() if l.strip()]
    return (lines + [""] * n)[:n]


def _parse_carousel(text: str) -> List[CarouselSlide]:
    slides = []
    blocks = re.split(r"\n(?=SLIDE\s*\d+)", text.strip(), flags=re.IGNORECASE)
    for block in blocks:
        m = re.match(r"SLIDE\s*(\d+)[:\n]+(.*)", block, re.DOTALL | re.IGNORECASE)
        if not m:
            continue
        num = int(m.group(1))
        body = m.group(2).strip()
        lines = body.splitlines()
        title = lines[0].strip() if lines else ""
        rest = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""
        slides.append(CarouselSlide(number=num, title=title, body=rest))
    return slides[:10]


class ContentWriter:
    def __init__(self, api_key: str):
        self._client = anthropic.Anthropic(api_key=api_key)

    def generate(self, brief: dict) -> PublicationPackage:
        sources = ", ".join(f['source'] for f in brief.get('fuentes', []))
        datos = ", ".join(brief.get('datos_clave', []))

        prompt = f"""Genera el paquete de publicación COMPLETO para esta historia.
Aplica REBEL BRAIN METHOD en todos los formatos.
Voz REBEL LUXURY: urbano-profesional, directo, técnico pero accesible, NUNCA genérico.

HISTORIA:
TÍTULO: {brief.get('titulo_principal', '')}
ÁNGULO NEUROCIENCIA: {brief.get('angulo_neurociencia', '')}
HOOK: {brief.get('hook_apertura', '')}
DATOS: {datos}
CONTROVERSIA: {brief.get('controversia', '')}
FUENTES: {sources}

---
FORMATO EXACTO (sin texto fuera de estas secciones):

SCRIPT_YOUTUBE:
[Guión completo 8-15 min en español. Pattern Interrupt primeros 5 seg. Aplica REBEL BRAIN METHOD completo. Mínimo 900 palabras.]

SCRIPT_SHORT:
[YouTube Shorts 55-58 seg. Solo el Pattern Interrupt + Rebel Reframe. Máximo 120 palabras.]

SCRIPT_INSTAGRAM_REEL:
[IG Reel 7-45 seg. Hook en 3 palabras + insight + reframe. Máximo 80 palabras.]

SCRIPT_TIKTOK:
[TikTok 21-90 seg. Lenguaje más urbano. Hook que rompe scroll. Máximo 150 palabras.]

SCRIPT_FACEBOOK_REEL:
[FB Reel 30-60 seg. Tono levemente más formal que TikTok. Máximo 100 palabras.]

CAROUSEL:
SLIDE 1:
[Título gancho — el que para el scroll]
[Copy 1-2 líneas]
SLIDE 2:
[Título]
[Copy]
SLIDE 3:
[Título]
[Copy]
SLIDE 4:
[Título]
[Copy]
SLIDE 5:
[Título]
[Copy]
SLIDE 6:
[Título]
[Copy]
SLIDE 7:
[Título]
[Copy]
SLIDE 8:
[Título: CTA implícito Rebel Luxury — sin "síguenos"]
[Copy cierre]

CAPTION_YOUTUBE:
[2-3 líneas debajo del título. Keyword principal + hook. Aparece sin expandir.]

CAPTION_INSTAGRAM:
[Hasta 2200 caracteres. Voz REBEL LUXURY. Hashtags al final: 3-5 grandes + 5-7 medianos + 4-5 de nicho.]

CAPTION_TIKTOK:
[Máximo 150 caracteres. Urbano. 3-5 hashtags.]

CAPTION_FACEBOOK:
[Máximo 400 caracteres. Profesional-urbano. Máximo 3 hashtags.]

YOUTUBE_TITLES:
1. [Keyword principal — promesa rebel luxury, máx 60 chars]
2. [Variante con ángulo neurociencia, máx 60 chars]
3. [Variante con controversia, máx 60 chars]

YOUTUBE_DESCRIPTION:
[Primeras 2 líneas con keyword + hook visible sin expandir. Luego timestamps 00:00, keywords secundarias, links placeholder.]"""

        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8192,
            system=[{"type": "text", "text": _SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": prompt}],
        )
        raw = response.content[0].text
        return self._parse(brief, raw)

    def _parse(self, brief: dict, raw: str) -> PublicationPackage:
        sections = [
            "SCRIPT_YOUTUBE", "SCRIPT_SHORT", "SCRIPT_INSTAGRAM_REEL",
            "SCRIPT_TIKTOK", "SCRIPT_FACEBOOK_REEL", "CAROUSEL",
            "CAPTION_YOUTUBE", "CAPTION_INSTAGRAM", "CAPTION_TIKTOK",
            "CAPTION_FACEBOOK", "YOUTUBE_TITLES", "YOUTUBE_DESCRIPTION",
        ]

        def get(start: str) -> str:
            idx = sections.index(start)
            end = sections[idx + 1] if idx + 1 < len(sections) else None
            return _section(raw, start, end)

        titles_raw = get("YOUTUBE_TITLES")
        carousel_raw = get("CAROUSEL")

        return PublicationPackage(
            brief=brief,
            script_es=get("SCRIPT_YOUTUBE"),
            script_short=get("SCRIPT_SHORT"),
            script_instagram_reel=get("SCRIPT_INSTAGRAM_REEL"),
            script_tiktok=get("SCRIPT_TIKTOK"),
            script_facebook_reel=get("SCRIPT_FACEBOOK_REEL"),
            carousel_slides=_parse_carousel(carousel_raw),
            caption_youtube=get("CAPTION_YOUTUBE"),
            captions_instagram=get("CAPTION_INSTAGRAM"),
            caption_tiktok=get("CAPTION_TIKTOK"),
            caption_facebook=get("CAPTION_FACEBOOK"),
            youtube_titles=_numbered_lines(titles_raw, 3),
            youtube_description=get("YOUTUBE_DESCRIPTION"),
        )
