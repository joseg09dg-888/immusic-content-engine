import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.content_engine.designer import Designer

d = Designer()
out = Path("logs/brand_assets")
out.mkdir(parents=True, exist_ok=True)

banner = d.generate_youtube_banner(
    tagline="NO LANZAMOS MUSICA. JAQUEAMOS MENTES.",
    handle="@IMMUSICSELLO",
    save_path=out / "youtube_banner.png",
    seed=0,
)
print(f"Banner generado: {banner.size} -> logs/brand_assets/youtube_banner.png")
