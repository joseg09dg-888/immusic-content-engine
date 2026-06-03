"""
Test script: Generate REBEL LUXURY creative output with Designer.
Topic: "La neurociencia detrás del éxito viral en música urbana"
Output: logs/test_run/
"""
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.content_engine.designer import Designer

TOPIC   = "La neurociencia detrás del éxito viral en música urbana"
SUBTITLE = "REBEL LUXURY · IM Music"
OUT_DIR  = PROJECT_ROOT / "logs" / "test_run"

CAROUSEL_SLIDES = [
    {
        "title": "El cerebro decide en 0.3 segundos",
        "body":  "Antes de que proceses la letra, el núcleo accumbens ya disparó dopamina.",
    },
    {
        "title": "El loop de anticipación",
        "body":  "Un hook viral activa el mismo circuito que una droga de diseño. No es metáfora.",
    },
    {
        "title": "La paradoja del tempo",
        "body":  "90-100 BPM sincroniza con el ritmo cardíaco en reposo. El cuerpo ya quiere seguirlo.",
    },
    {
        "title": "Frecuencias que el cerebro recuerda",
        "body":  "432 Hz vs 440 Hz: no es superstición, hay estudios de resonancia cortical.",
    },
    {
        "title": "Identidad antes que calidad",
        "body":  "Feid no vende canciones, vende una identidad. El cerebro compra personas, no notas.",
    },
    {
        "title": "El efecto de la escasez auditiva",
        "body":  "Silencio estratégico genera más tensión que cualquier instrumento. La ausencia tiene peso.",
    },
    {
        "title": "Neuromarketing de portadas",
        "body":  "El ojo fija la portada antes de escuchar. Oscuridad + contraste = señal de autoridad.",
    },
    {
        "title": "La regla del 7 en streaming",
        "body":  "7 escuchas crean familiaridad neurológica. Los algoritmos calculan retención, no gustos.",
    },
]


def report_image(label: str, img, path: Path):
    size_kb = path.stat().st_size // 1024 if path.exists() else 0
    print(f"  [{label}]")
    print(f"    Path:       {path}")
    print(f"    Dimensions: {img.size[0]} x {img.size[1]} px")
    print(f"    File size:  {size_kb} KB")


def main():
    print("=" * 60)
    print("IM MUSIC — REBEL LUXURY  |  Designer Test Run")
    print("=" * 60)
    print(f"Topic:   {TOPIC}")
    print(f"Out dir: {OUT_DIR}")
    print()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    d = Designer()

    # ── Thumbnail ────────────────────────────────────────────────
    print("Generating thumbnail (YouTube 1280×720) …")
    thumb_path = OUT_DIR / "thumbnail.png"
    thumb = d.generate_thumbnail(TOPIC, SUBTITLE, save_path=thumb_path)
    report_image("thumbnail", thumb, thumb_path)
    print()

    # ── Story ────────────────────────────────────────────────────
    print("Generating story (Instagram/TikTok 1080×1920) …")
    story_path = OUT_DIR / "story.png"
    story = d.generate_story(TOPIC, SUBTITLE, save_path=story_path)
    report_image("story", story, story_path)
    print()

    # ── TikTok Cover ─────────────────────────────────────────────
    print("Generating TikTok cover (1080×1920) …")
    tiktok_path = OUT_DIR / "tiktok_cover.png"
    tiktok = d.generate_tiktok_cover(TOPIC, save_path=tiktok_path)
    report_image("tiktok_cover", tiktok, tiktok_path)
    print()

    # ── Carousel ─────────────────────────────────────────────────
    print(f"Generating carousel ({len(CAROUSEL_SLIDES)} slides, Instagram 1080×1080) …")
    carousel_dir = OUT_DIR / "carousel"
    slides = d.generate_carousel(CAROUSEL_SLIDES, save_dir=carousel_dir)
    for i, img in enumerate(slides):
        slide_path = carousel_dir / f"slide_{i+1:02d}.png"
        report_image(f"slide_{i+1:02d}", img, slide_path)
    print()

    # ── Summary ──────────────────────────────────────────────────
    all_files = list(OUT_DIR.rglob("*.png"))
    print("=" * 60)
    print(f"TOTAL FILES GENERATED: {len(all_files)}")
    total_kb = sum(f.stat().st_size for f in all_files) // 1024
    print(f"TOTAL SIZE:            {total_kb} KB")
    print("=" * 60)
    for f in sorted(all_files):
        rel = f.relative_to(OUT_DIR)
        print(f"  {rel}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()
