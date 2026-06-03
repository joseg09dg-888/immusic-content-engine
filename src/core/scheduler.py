"""IM Music Scheduler — Pipeline orchestrator L/M/V (Mon/Wed/Fri)."""
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.brand import Brand
from core.config import Config
from content_engine.research import ResearchEngine
from content_engine.writer import ContentWriter
from content_engine.designer import Designer
from content_engine.seo_engine import SEOEngine

logger = logging.getLogger(__name__)
COT = timezone(timedelta(hours=-5))


class ContentScheduler:
    PUBLISH_DAYS = {0, 2, 4}  # Mon, Wed, Fri

    def __init__(self):
        self.config = Config()
        self.research = ResearchEngine()
        self.writer = ContentWriter()
        self.designer = Designer()
        self.seo = SEOEngine()

    def is_publish_day(self, dt: Optional[datetime] = None) -> bool:
        return (dt or datetime.now(COT)).weekday() in self.PUBLISH_DAYS

    def run_content_pipeline(self, topic: Optional[str] = None, dry_run: bool = True) -> dict:
        """Full content pipeline. dry_run=True generates assets but does not publish."""
        logger.info("=== IM Music Content Pipeline START ===")

        # 1. Research
        if topic:
            brief = self.research.build_brief(
                titulo_principal=topic,
                angulo_neurociencia="neurociencia aplicada a la industria musical",
                hook_apertura=f"Lo que nadie te dice sobre {topic}",
                datos_clave=[], controversia="La industria lo sabe y lo oculta", fuentes=["IM Music"],
            )
        else:
            stories = self.research.fetch_top_stories(limit=5)
            brief = self.research.score_and_select(stories)

        # 2. Content generation
        content = {}
        content["youtube_script"] = self.writer.generate_youtube_script(brief)
        if hasattr(self.writer, "generate_youtube_short"):
            content["youtube_short"] = self.writer.generate_youtube_short(brief)
        if hasattr(self.writer, "generate_instagram_reel"):
            content["instagram_reel"] = self.writer.generate_instagram_reel(brief)
        if hasattr(self.writer, "generate_tiktok_carousel"):
            content["tiktok_carousel"] = self.writer.generate_tiktok_carousel(brief)
        if hasattr(self.writer, "generate_youtube_monetization_pack"):
            content["monetization_pack"] = self.writer.generate_youtube_monetization_pack(brief)

        # 3. SEO
        title = brief.get("titulo_principal", "IM Music")
        content["seo_youtube"] = self.seo.generate_youtube_title_and_tags(title, brief.get("fuentes", []))
        if hasattr(self.seo, "tiktok_seo_complete"):
            content["seo_tiktok"] = self.seo.tiktok_seo_complete(title, brief)

        # 4. Visual assets
        output_dir = Path("releases") / f"content_{datetime.now(COT).strftime('%Y-%m-%d_%H%M')}"
        output_dir.mkdir(parents=True, exist_ok=True)

        assets = {}
        assets["youtube_thumbnail"] = str(output_dir / "youtube_thumbnail.png")
        self.designer.generate_thumbnail(title, save_path=Path(assets["youtube_thumbnail"]))
        assets["story"] = str(output_dir / "instagram_story.png")
        self.designer.generate_story(title, save_path=Path(assets["story"]))
        assets["tiktok_cover"] = str(output_dir / "tiktok_cover.png")
        self.designer.generate_tiktok_cover(title, save_path=Path(assets["tiktok_cover"]))
        if hasattr(self.designer, "generate_youtube_short_thumbnail"):
            assets["youtube_short_thumb"] = str(output_dir / "youtube_short_thumbnail.png")
            self.designer.generate_youtube_short_thumbnail(title, save_path=Path(assets["youtube_short_thumb"]))
        carousel_dir = output_dir / "carousel"
        self.designer.generate_carousel(title, brief.get("datos_clave", []), save_dir=carousel_dir)
        assets["carousel_dir"] = str(carousel_dir)

        if not dry_run:
            raise NotImplementedError(
                "Publishing requires OAuth credentials. Set GOOGLE_CLIENT_ID + GOOGLE_CLIENT_SECRET in .env"
            )

        logger.info(f"Pipeline complete. Output: {output_dir}")
        return {"brief": brief, "content": content, "assets": assets, "output_dir": str(output_dir)}
