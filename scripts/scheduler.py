"""
IM Music — Scheduler Automático
Publica contenido L/M/V a las 18:00 hora Colombia (UTC-5 = 23:00 UTC)

Instalar: pip install apscheduler
Correr:   python scripts/scheduler.py
Correr en background: pythonw scripts/scheduler.py  (sin consola)
"""
import sys
import io
import logging
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

LOG_FILE = ROOT / "logs" / "scheduler.log"
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler(str(LOG_FILE), encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("scheduler")


def publish_job():
    """Corre el pipeline completo: genera + sube a YouTube + Instagram + TikTok."""
    log.info("=" * 50)
    log.info("PIPELINE INICIADO — %s", datetime.now().strftime("%Y-%m-%d %H:%M"))
    try:
        from scripts.pipeline import run
        import argparse
        args = argparse.Namespace(
            topic="",
            dry_run=False,
            youtube_only=False,
            instagram_only=False,
            tiktok_only=False,
        )
        work_dir = run(args)
        log.info("PIPELINE OK — %s", work_dir)
    except Exception as e:
        log.error("PIPELINE ERROR: %s", e, exc_info=True)


def main():
    try:
        from apscheduler.schedulers.blocking import BlockingScheduler
        from apscheduler.triggers.cron import CronTrigger
    except ImportError:
        log.error("apscheduler no instalado. Ejecuta: pip install apscheduler")
        sys.exit(1)

    scheduler = BlockingScheduler(timezone="America/Bogota")

    # L/M/V a las 18:00 hora Colombia
    scheduler.add_job(
        publish_job,
        CronTrigger(day_of_week="mon,wed,fri", hour=18, minute=0,
                    timezone="America/Bogota"),
        id="immusic_content",
        name="IM Music REBEL LUXURY Content",
        max_instances=1,
        coalesce=True,
    )

    log.info("Scheduler activo — publicando L/M/V 18:00 Bogota")
    log.info("Proxima ejecucion: %s",
             scheduler.get_job("immusic_content").next_run_time)

    try:
        scheduler.start()
    except KeyboardInterrupt:
        log.info("Scheduler detenido")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
