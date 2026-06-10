"""
IM Music — Autopilot Diario
Genera el pack completo del dia (imagenes + narracion + 2 videos + beat),
SIN publicar nada. Pensado para correr solo L/M/V 8:00 AM COT via el
Programador de tareas de Windows.

La publicacion real queda en manos de scripts/aprobar_publicar.py,
despues de que revises el contenido.

Uso:
    python scripts/autopilot_diario.py
"""
import sys
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402
from src.core.drive_sync import sync_pack_to_drive  # noqa: E402


def main():
    args = argparse.Namespace(
        topic="", dry_run=True,
        youtube_only=False, instagram_only=False, tiktok_only=False,
    )
    work_dir = pipeline.run(args)

    brief = json.loads((work_dir / "brief.json").read_text(encoding="utf-8"))
    drive_dest = sync_pack_to_drive(work_dir, brief["titulo_principal"])

    rel = work_dir.relative_to(ROOT)
    print(f"\n{'='*60}")
    print("  LISTO PARA APROBAR")
    print(f"  Local: {work_dir}")
    if drive_dest:
        print(f"  Drive: {drive_dest}")
    print()
    print("  Para publicar en YouTube + Instagram + TikTok:")
    print(f"    python scripts/aprobar_publicar.py {rel}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
