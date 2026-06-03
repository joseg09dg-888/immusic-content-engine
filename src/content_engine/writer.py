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

    def _call_api(self, prompt: str, max_tokens: int = 2048) -> str:
        response = self._client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            system=[{"type": "text", "text": _SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}],
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def generate_youtube_short(self, brief: dict) -> dict:
        prompt = f"""Crea guión YouTube Short 55-58 segundos sobre: "{brief.get('titulo_principal', '')}"
Ángulo neurociencia: {brief.get('angulo_neurociencia', '')}

ESTRUCTURA OBLIGATORIA:
- 0-3s: Pattern Interrupt — rompe el scroll con frase o visual impactante
- 3-15s: Dato sorprendente con número concreto
- 15-45s: Neurociencia explicada — técnico pero accesible, voz REBEL LUXURY
- 45-55s: Rebel Reframe — la verdad que nadie te dijo
- 55-58s: CTA IM Music — directo, sin pedir permiso

Responde EXACTAMENTE en este formato JSON (sin texto fuera del JSON):
{{
  "guion_completo": "guión completo hablado de 55-58 segundos",
  "texto_pantalla": ["texto slide 1", "texto slide 2", "texto slide 3", "texto slide 4", "texto slide 5"],
  "hook_visual": "descripción del gancho visual primeros 3 segundos",
  "hashtags_youtube_short": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5"]
}}"""
        raw = self._call_api(prompt, max_tokens=1200)
        return self._parse_json(raw)

    def generate_tiktok_carousel(self, brief: dict, num_slides: int = 6) -> dict:
        prompt = f"""Crea carrusel {num_slides} slides TikTok sobre: "{brief.get('titulo_principal', '')}"
Ángulo neurociencia: {brief.get('angulo_neurociencia', '')}
Hook: {brief.get('hook_apertura', '')}

REGLAS POR SLIDE:
- Slide 1: título impactante máximo 6 palabras — para el scroll
- Slides 2 a {num_slides - 1}: insight poderoso máximo 15 palabras por slide
- Slide {num_slides}: verdad incómoda como CTA — sin "síguenos" ni genéricos

Responde EXACTAMENTE en este formato JSON (sin texto fuera del JSON):
{{
  "slides": [
    {{"numero": 1, "titulo": "título máx 6 palabras", "subtitulo": "subtítulo opcional", "dato": "dato o stat si aplica"}},
    {{"numero": 2, "titulo": "insight poderoso máx 15 palabras", "subtitulo": "", "dato": ""}},
    {{"numero": 3, "titulo": "insight poderoso máx 15 palabras", "subtitulo": "", "dato": ""}},
    {{"numero": 4, "titulo": "insight poderoso máx 15 palabras", "subtitulo": "", "dato": ""}},
    {{"numero": 5, "titulo": "insight poderoso máx 15 palabras", "subtitulo": "", "dato": ""}},
    {{"numero": {num_slides}, "titulo": "verdad incómoda CTA máx 15 palabras", "subtitulo": "", "dato": ""}}
  ],
  "caption_tiktok": "caption TikTok máximo 150 caracteres con 3-5 hashtags"
}}"""
        raw = self._call_api(prompt, max_tokens=1500)
        return self._parse_json(raw)

    def generate_instagram_reel(self, brief: dict) -> dict:
        prompt = f"""Crea guión Instagram Reel 15-30 segundos sobre: "{brief.get('titulo_principal', '')}"
Ángulo neurociencia: {brief.get('angulo_neurociencia', '')}

ESTRUCTURA OBLIGATORIA:
- 0-3s: Hook visual — 3 palabras máximo en pantalla, acción que detiene el scroll
- 3-20s: Core insight neurociencia — técnico y accesible, voz REBEL LUXURY
- 20-28s: Rebel Reframe — la perspectiva que nadie más da
- 28-30s: IM Music brand moment — identidad, no CTA genérico

Responde EXACTAMENTE en este formato JSON (sin texto fuera del JSON):
{{
  "guion_escenas": [
    {{"tiempo": "0-3s", "accion": "descripción acción visual", "texto_pantalla": "texto en pantalla", "narracion": "narración hablada"}},
    {{"tiempo": "3-20s", "accion": "descripción acción visual", "texto_pantalla": "texto en pantalla", "narracion": "narración hablada"}},
    {{"tiempo": "20-28s", "accion": "descripción acción visual", "texto_pantalla": "texto en pantalla", "narracion": "narración hablada"}},
    {{"tiempo": "28-30s", "accion": "descripción acción visual", "texto_pantalla": "texto en pantalla", "narracion": "narración hablada"}}
  ],
  "caption_instagram": "caption completo hasta 2200 caracteres voz REBEL LUXURY con hashtags",
  "hashtags_instagram": ["#hashtag1", "#hashtag2", "#hashtag3", "#hashtag4", "#hashtag5", "#hashtag6", "#hashtag7", "#hashtag8", "#hashtag9", "#hashtag10"]
}}"""
        raw = self._call_api(prompt, max_tokens=1400)
        return self._parse_json(raw)

    def generate_youtube_monetization_pack(self, brief: dict, video_duration_min: int = 8) -> dict:
        prompt = f"""Crea pack monetización YouTube para video {video_duration_min} minutos sobre: "{brief.get('titulo_principal', '')}"
Ángulo neurociencia: {brief.get('angulo_neurociencia', '')}
Hook: {brief.get('hook_apertura', '')}

GENERAR LOS 6 COMPONENTES:

1. CAPÍTULOS: mínimo 5 capítulos en formato "0:00 Título del capítulo" — distribuidos estratégicamente en los {video_duration_min} minutos
2. DESCRIPCIÓN SEO: primeras 2 líneas con keyword principal + hook visible sin expandir, luego timestamps, keywords secundarias, links placeholders [LINK_1] [LINK_2] [LINK_3], créditos IM Music al final
3. PINNED COMMENT: pregunta de debate que genere respuestas, máximo 200 caracteres
4. END SCREEN SCRIPT: texto hablado exacto para los últimos 20 segundos del video — natural, no robótico
5. COMMUNITY POST: post para publicar 24h antes del video — genera expectativa sin spoilear
6. TAGS YOUTUBE: exactamente 30 tags relevantes para el algoritmo

Responde EXACTAMENTE en este formato JSON (sin texto fuera del JSON):
{{
  "capitulos": ["0:00 Título", "1:30 Título", "3:00 Título", "5:00 Título", "7:00 Título"],
  "descripcion_seo": "descripción SEO completa con timestamps, keywords, links placeholder y créditos",
  "pinned_comment": "pregunta debate máximo 200 caracteres",
  "end_screen_script": "texto hablado últimos 20 segundos natural y fluido",
  "community_post": "post comunidad para publicar 24h antes del video",
  "tags_youtube": ["tag1", "tag2", "tag3", "tag4", "tag5", "tag6", "tag7", "tag8", "tag9", "tag10", "tag11", "tag12", "tag13", "tag14", "tag15", "tag16", "tag17", "tag18", "tag19", "tag20", "tag21", "tag22", "tag23", "tag24", "tag25", "tag26", "tag27", "tag28", "tag29", "tag30"]
}}"""
        raw = self._call_api(prompt, max_tokens=2500)
        return self._parse_json(raw)

    def _parse_json(self, raw: str) -> dict:
        import json
        raw = raw.strip()
        # Extract JSON block if wrapped in markdown code fences
        fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", raw, re.DOTALL)
        if fence_match:
            raw = fence_match.group(1)
        else:
            # Find first { and last } to extract JSON object
            start = raw.find("{")
            end = raw.rfind("}") + 1
            if start != -1 and end > start:
                raw = raw[start:end]
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            logger.warning("JSON parse failed: %s — returning raw text", e)
            return {"raw": raw}

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
