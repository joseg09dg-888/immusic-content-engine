"""
End-to-end smoke test FASE 1.
Requires ANTHROPIC_API_KEY in .env
Output: logs/test_pub_output.json
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.core.config import config
from src.core.brand import Brand
from src.content_engine.research import ResearchEngine
from src.content_engine.writer import ContentWriter

_FALLBACK_BRIEF = {
    "titulo_principal": "La neurociencia detrás del éxito viral en música 2026",
    "angulo_neurociencia": "El loop de dopamina y cómo los sellos lo explotan",
    "hook_apertura": "¿Sabías que tu cerebro decide si una canción es viral antes de escuchar el segundo compás?",
    "datos_clave": [
        "88% de los oyentes eligen música por estado de ánimo",
        "El primer beat determina el 70% de la decisión de escucha",
    ],
    "controversia": "Los algoritmos de Spotify conocen tus emociones mejor que tú",
    "fuentes": [{"source": "IM Music Research", "url": "https://immusic.co"}],
}


def main():
    sep = "=" * 60
    print(f"\n{sep}")
    print(f"  IM Music Content Engine — FASE 1 Test")
    print(f"  {Brand.CONCEPT} | {Brand.LABEL} | {Brand.HANDLE}")
    print(f"{sep}\n")

    print("[ 1/3 ] Research...")
    engine = ResearchEngine()
    brief = engine.run()
    if not brief:
        print("  No RSS stories — using fallback brief.")
        brief = _FALLBACK_BRIEF
    print(f"  Story: {brief['titulo_principal'][:70]}")

    print("\n[ 2/3 ] Writing with Claude API...")
    writer = ContentWriter(api_key=config.ANTHROPIC_API_KEY)
    pkg = writer.generate(brief)
    print(f"  Script: {len(pkg.script_es)} chars")
    print(f"  Instagram: {len(pkg.captions_instagram)} chars")
    print(f"  TikTok: {pkg.caption_tiktok[:60]}...")
    print(f"  YT title: {pkg.youtube_titles[0][:60]}")

    print("\n[ 3/3 ] Saving...")
    output = {
        "brief": pkg.brief,
        "script_es": pkg.script_es,
        "captions_instagram": pkg.captions_instagram,
        "caption_tiktok": pkg.caption_tiktok,
        "youtube_titles": pkg.youtube_titles,
        "youtube_description": pkg.youtube_description,
        "brand": {"label": Brand.LABEL, "concept": Brand.CONCEPT, "colors": Brand.palette()},
    }
    out = Path("logs/test_pub_output.json")
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Saved: {out.resolve()}")
    print(f"\n{sep}")
    print("  FASE 1 COMPLETE ✅")
    print(f"{sep}\n")


if __name__ == "__main__":
    main()
