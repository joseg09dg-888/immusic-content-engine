import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from pathlib import Path
from src.content_engine.designer import Designer

d = Designer()
out = Path("logs/test_fix")
out.mkdir(parents=True, exist_ok=True)

post = d.generate_post(
    hook="NO LANZAMOS MUSICA, NI SUBIMOS VIDEOS AL AZAR",
    headline="JAQUEAMOS MENTES",
    cta="DESCUBRE COMO EN NUESTRO CANAL",
    save_path=out / "post_test.png",
    seed=0,
)
print(f"post:  {post.size}")

story = d.generate_story(
    hook="COMO LOGRAMOS RESULTADOS QUE OTROS",
    headline="SOLO SUENAN",
    cta="VER EN NUESTRO CANAL",
    save_path=out / "story_test.png",
    seed=1,
)
print(f"story: {story.size}")

thumb = d.generate_thumbnail(
    hook="LA ESTRATEGIA QUE NADIE EXPLICA",
    headline="REBEL LUXURY",
    cta="IM MUSIC SELLO",
    save_path=out / "thumb_test.png",
    seed=2,
)
print(f"thumb: {thumb.size}")

print("OK - generados en logs/test_fix/")
