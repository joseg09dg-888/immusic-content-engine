import pytest
from pathlib import Path
from PIL import Image
from src.core.brand import Brand, Dimensions
from src.content_engine.designer import Designer, _violet_bg, _black_bg, _draw_rebel_text


def test_violet_bg_correct_size():
    img = _violet_bg((1280, 720))
    assert img.size == (1280, 720)
    assert img.mode == "RGB"


def test_violet_bg_is_violet():
    img = _violet_bg((100, 100), seed=1)
    r, g, b = img.getpixel((50, 50))
    assert r > 60 and b > 200


def test_violet_bg_different_seeds_differ():
    img1 = _violet_bg((200, 200), seed=1)
    img2 = _violet_bg((200, 200), seed=2)
    assert img1.tobytes() != img2.tobytes()


def test_black_bg_correct_size():
    img = _black_bg((1280, 720))
    assert img.size == (1280, 720)
    assert img.mode == "RGB"


def test_black_bg_is_dark():
    img = _black_bg((100, 100), seed=1)
    r, g, b = img.getpixel((2, 2))
    assert r < 40 and g < 20 and b < 40


def test_thumbnail_correct_size():
    d = Designer()
    img = d.generate_thumbnail("Test Hook", "Test Title")
    assert img.size == Dimensions.YOUTUBE_THUMBNAIL
    assert img.mode == "RGB"


def test_thumbnail_saves_file(tmp_path):
    d = Designer()
    out = tmp_path / "thumb.png"
    d.generate_thumbnail("Hook", "Title", save_path=out)
    assert out.exists()
    assert Image.open(out).size == Dimensions.YOUTUBE_THUMBNAIL


def test_post_correct_size():
    d = Designer()
    img = d.generate_post("Hook text", "HEADLINE")
    assert img.size == Dimensions.INSTAGRAM_POST   # 1080x1350 (4:5 portrait, igual al Canva)
    assert img.mode == "RGB"


def test_story_correct_size():
    d = Designer()
    img = d.generate_story("Hook", "Story Title")
    assert img.size == Dimensions.INSTAGRAM_STORY


def test_tiktok_cover_correct_size():
    d = Designer()
    img = d.generate_tiktok_cover("Hook", "TikTok Title")
    assert img.size == Dimensions.TIKTOK_COVER


def test_carousel_returns_correct_count(tmp_path):
    d = Designer()
    slides = [{"headline": f"Slide {i}", "body": "Content"} for i in range(8)]
    paths = d.generate_carousel(slides, save_dir=tmp_path / "carousel")
    assert len(paths) == 8
    for p in paths:
        assert Image.open(p).size == Dimensions.INSTAGRAM_REEL  # 9:16 vertical


def test_carousel_caps_at_10(tmp_path):
    d = Designer()
    slides = [{"headline": f"Slide {i}", "body": "x"} for i in range(15)]
    paths = d.generate_carousel(slides, save_dir=tmp_path / "carousel2")
    assert len(paths) == 10


def test_generate_pack_creates_all_files(tmp_path):
    d = Designer()
    brief = {
        "titulo_principal": "LA NEUROCIENCIA DEL HIT",
        "angulo_neurociencia": "Por que repites la misma cancion",
        "hook_apertura": "95% de las decisiones musicales son inconscientes",
        "datos_clave": ["Dopamina activa en pre-chorus", "El cerebro predice el drop"],
        "controversia": "Las plataformas explotan esto",
        "fuentes": ["Nature 2024"],
    }
    pack = d.generate_pack(brief, tmp_path)
    assert "post" in pack
    assert "thumbnail" in pack
    assert "story" in pack
    assert "tiktok" in pack
    assert "carousel" in pack
    assert len(pack["carousel"]) >= 3
    assert (tmp_path / "post.png").exists()
    assert Image.open(tmp_path / "post.png").size == Dimensions.INSTAGRAM_POST
    assert (tmp_path / "thumbnail.png").exists()
    assert (tmp_path / "story.png").exists()
