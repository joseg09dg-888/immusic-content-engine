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
    return (lines + ["", "", ""])[:3]


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

Responde EXACTAMENTE en este formato:

SCRIPT:
[Guión completo YouTube en español, 5-8 minutos ~800-1200 palabras, aplicando REBEL BRAIN METHOD]

CAPTIONS_INSTAGRAM:
[Caption hasta 2200 caracteres + hashtags #RebelLuxury #IMMusic]

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

        return PublicationPackage(
            brief=brief,
            script_es=script,
            captions_instagram=captions_ig,
            caption_tiktok=caption_tt,
            youtube_titles=_parse_numbered_list(titles_raw),
            youtube_description=yt_desc,
        )
