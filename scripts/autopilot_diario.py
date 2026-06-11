"""
IM Music — Autopilot Diario
Genera el pack completo del dia (imagenes + narracion + 2 videos + beat),
SIN publicar nada. Pensado para correr solo L/M/V 8:00 AM COT via el
Programador de tareas de Windows.

La publicacion real queda en manos de scripts/aprobar_publicar.py,
despues de que revises el contenido.

Antes de generar, borra packs viejos (> RETENTION_DAYS) que nunca se
aprobaron — local y en Drive — para no llenar el almacenamiento.

Uso:
    python scripts/autopilot_diario.py
"""
import sys
import json
import shutil
import argparse
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import pipeline  # noqa: E402
from src.core.drive_sync import sync_pack_to_drive, delete_pack_from_drive  # noqa: E402

RETENTION_DAYS = 5


def cleanup_unapproved_packs():
    """Borra runs sin APROBADO.txt mas viejos de RETENTION_DAYS (local + Drive)."""
    releases_dir = ROOT / "releases"
    if not releases_dir.exists():
        return

    cutoff = datetime.now() - timedelta(days=RETENTION_DAYS)
    for run_dir in sorted(releases_dir.glob("run_*")):
        if (run_dir / "APROBADO.txt").exists():
            continue
        try:
            ts = datetime.strptime(run_dir.name, "run_%Y%m%d_%H%M%S")
        except ValueError:
            continue
        if ts >= cutoff:
            continue

        brief_file = run_dir / "brief.json"
        if brief_file.exists():
            brief = json.loads(brief_file.read_text(encoding="utf-8"))
            delete_pack_from_drive(brief.get("titulo_principal", "pack"), ts)

        shutil.rmtree(run_dir)
        print(f"[Cleanup] Borrado pack no aprobado: {run_dir.name}")


def main():
    cleanup_unapproved_packs()

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
