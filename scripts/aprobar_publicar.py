"""
IM Music — Aprobar y Publicar
Toma un pack ya generado (releases/run_*) y lo publica en YouTube,
Instagram y TikTok. Este es el unico paso que toca las redes —
correlo solo despues de revisar el contenido.

Uso:
    python scripts/aprobar_publicar.py                  # ultimo pack generado
    python scripts/aprobar_publicar.py releases/run_20260610_121354
    python scripts/aprobar_publicar.py --youtube-only
    python scripts/aprobar_publicar.py --instagram-only
    python scripts/aprobar_publicar.py --tiktok-only
"""
import sys
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402


def find_latest_run() -> Path:
    runs = sorted((ROOT / "releases").glob("run_*"), key=lambda p: p.name)
    if not runs:
        print("[ERROR] No hay packs generados en releases/. Corre primero:")
        print("  python scripts/autopilot_diario.py")
        sys.exit(1)
    return runs[-1]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("work_dir", nargs="?", default="")
    p.add_argument("--youtube-only", action="store_true")
    p.add_argument("--instagram-only", action="store_true")
    p.add_argument("--tiktok-only", action="store_true")
    args = p.parse_args()

    work_dir = Path(args.work_dir) if args.work_dir else find_latest_run()
    if not work_dir.is_absolute():
        work_dir = ROOT / work_dir
    if not work_dir.exists():
        print(f"[ERROR] No existe: {work_dir}")
        sys.exit(1)

    brief_file = work_dir / "brief.json"
    if not brief_file.exists():
        print(f"[ERROR] No se encontro brief.json en {work_dir}")
        print("  (Este pack fue generado antes de la version con aprobacion)")
        sys.exit(1)
    brief = json.loads(brief_file.read_text(encoding="utf-8"))

    short_path = work_dir / "short.mp4"
    long_path = work_dir / "video_canal.mp4"
    thumb_path = work_dir / "thumbnail.png"
    carousel_paths = sorted((work_dir / "carousel").glob("slide_*.png"))

    ok_short = short_path.exists()
    ok_long = long_path.exists()

    print(f"\n{'='*60}")
    print("  IM MUSIC — REBEL LUXURY — APROBAR Y PUBLICAR")
    print(f"  Pack: {work_dir.name}")
    print(f"  Tema: {brief.get('titulo_principal', '')}")
    print(f"{'='*60}")

    results = {}

    if not args.instagram_only and not args.tiktok_only:
        print("\n  YouTube Shorts:")
        if ok_short:
            results["yt_short"] = pipeline.publish_youtube(
                short_path, brief, thumb_path if thumb_path.exists() else None, is_short=True)
        else:
            print("     [SKIP] short.mp4 no existe")

        print("  YouTube Canal:")
        if ok_long:
            results["yt_long"] = pipeline.publish_youtube(
                long_path, brief, thumb_path if thumb_path.exists() else None, is_short=False)
        else:
            print("     [SKIP] video_canal.mp4 no existe")

    if not args.youtube_only and not args.tiktok_only:
        print("\n  Instagram (carrusel):")
        if carousel_paths:
            results["ig_carousel"] = pipeline.publish_instagram_carousel(carousel_paths, brief)
        else:
            print("     [SKIP] no hay slides de carrusel")

    if not args.youtube_only and not args.instagram_only:
        print("\n  TikTok:")
        target = short_path if ok_short else (work_dir / "story.png")
        results["tiktok"] = pipeline.publish_tiktok(target, brief)

    print(f"\n{'='*60}")
    print("  RESUMEN")
    print(f"{'='*60}")
    print(f"  YouTube Short:   {'OK' if results.get('yt_short') else 'SKIP/FAIL'}")
    print(f"  YouTube Canal:   {'OK' if results.get('yt_long') else 'SKIP/FAIL'}")
    print(f"  Instagram Carr.: {'OK' if results.get('ig_carousel') else 'SKIP/FAIL'}")
    print(f"  TikTok:          {'OK' if results.get('tiktok') else 'SKIP/FAIL'}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
