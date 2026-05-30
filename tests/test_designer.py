import pytest
from pathlib import Path
from PIL import Image
from src.core.brand import Brand, Dimensions
from src.content_engine.designer import Designer, _sketch_galaxy_bg, _pick_template, _TEMPLATES


def test_galaxy_bg_correct_size():
    img = _sketch_galaxy_bg((1280, 720))
    assert img.size == (1280, 720)
    assert img.mode == "RGB"


def test_galaxy_bg_is_dark():
    img = _sketch_galaxy_bg((100, 100), seed=1)
    raw = img.tobytes()
    avg = sum(raw) / len(raw)
    assert avg < 80  # background is predominantly dark


def test_galaxy_bg_different_seeds_differ():
    img1 = _sketch_galaxy_bg((200, 200), seed=1)
    img2 = _sketch_galaxy_bg((200, 200), seed=2)
    assert img1.tobytes() != img2.tobytes()


def test_pick_template_returns_valid():
    t = _pick_template("any title")
    assert t in _TEMPLATES
    assert "star_density" in t
    assert "text_anchor" in t


def test_pick_template_deterministic():
    assert _pick_template("hello") == _pick_template("hello")


def test_thumbnail_correct_size():
    d = Designer()
    img = d.generate_thumbnail("Test Title")
    assert img.size == Dimensions.YOUTUBE_THUMBNAIL
    assert img.mode == "RGB"


def test_thumbnail_saves_file(tmp_path):
    d = Designer()
    out = tmp_path / "thumb.png"
    d.generate_thumbnail("Test", save_path=out)
    assert out.exists()
    loaded = Image.open(out)
    assert loaded.size == Dimensions.YOUTUBE_THUMBNAIL


def test_story_correct_size():
    d = Designer()
    img = d.generate_story("Story Title")
    assert img.size == Dimensions.INSTAGRAM_STORY


def test_tiktok_cover_correct_size():
    d = Designer()
    img = d.generate_tiktok_cover("TikTok Title")
    assert img.size == Dimensions.TIKTOK_COVER


def test_carousel_returns_correct_count():
    d = Designer()
    slides = [{"title": f"Slide {i}", "body": "Content"} for i in range(8)]
    imgs = d.generate_carousel(slides)
    assert len(imgs) == 8
    assert all(img.size == Dimensions.INSTAGRAM_SQUARE for img in imgs)


def test_carousel_caps_at_10():
    d = Designer()
    slides = [{"title": f"Slide {i}", "body": "x"} for i in range(15)]
    imgs = d.generate_carousel(slides)
    assert len(imgs) == 10


def test_generate_pack_creates_all_files(tmp_path):
    d = Designer()
    pack = d.generate_pack("Pack Title", "Subtitle", tmp_path)
    assert "thumbnail" in pack
    assert "story" in pack
    assert "tiktok_cover" in pack
    assert "carousel" in pack
    assert len(pack["carousel"]) == 8
    assert (tmp_path / "thumbnail.png").exists()
    assert (tmp_path / "story.png").exists()
