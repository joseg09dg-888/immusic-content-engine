from src.content_engine.seo_engine import SEOEngine
from src.core.brand import Brand


def test_youtube_titles_count():
    seo = SEOEngine()
    titles = seo.youtube_titles("neuromarketing musical", "impacto en el consumidor")
    assert len(titles) == 3


def test_youtube_titles_max_length():
    seo = SEOEngine()
    titles = seo.youtube_titles("neuromarketing musical", "impacto en el consumidor")
    assert all(len(t) <= 60 for t in titles)


def test_youtube_tags_count():
    seo = SEOEngine()
    tags = seo.youtube_tags("marketing musical", genre="chill hop")
    assert 10 <= len(tags) <= 20


def test_youtube_tags_include_genre_chill():
    seo = SEOEngine()
    tags = seo.youtube_tags("study beats", genre="chill hop")
    joined = " ".join(tags).lower()
    assert "chill" in joined or "lofi" in joined


def test_youtube_tags_include_genre_afro():
    seo = SEOEngine()
    tags = seo.youtube_tags("afro beats", genre="afro house")
    joined = " ".join(tags).lower()
    assert "afro" in joined or "house" in joined


def test_channel_tags_max_500():
    seo = SEOEngine()
    tags = seo.youtube_channel_tags()
    assert len(tags) <= 500
    assert Brand.LABEL in tags


def test_channel_description_has_brand():
    seo = SEOEngine()
    desc = seo.youtube_channel_description()
    assert Brand.LABEL in desc
    assert "Medellín" in desc or "Colombia" in desc


def test_instagram_hashtags_format():
    seo = SEOEngine()
    tags = seo.instagram_hashtags("neurociencia")
    assert "#IMMusic" in tags or "#RebelLuxury" in tags
    assert tags.count("#") >= 10


def test_instagram_hashtags_not_too_many():
    seo = SEOEngine()
    tags = seo.instagram_hashtags()
    assert tags.count("#") <= 18


def test_instagram_bio_has_handle():
    seo = SEOEngine()
    bio = seo.instagram_bio()
    assert Brand.LABEL in bio
    assert "Medellín" in bio


def test_tiktok_hashtags_few():
    seo = SEOEngine()
    tags = seo.tiktok_hashtags()
    assert 3 <= tags.count("#") <= 8


def test_song_metadata_structure():
    seo = SEOEngine()
    meta = seo.song_metadata("Galaxia Profunda", "Chill Hop", bpm=90)
    assert meta["title"] == "Galaxia Profunda"
    assert meta["bpm"] == 90
    assert meta["artist"] == Brand.LABEL
    assert meta["isrc"].startswith("CO-IMM-")
    assert "Chill Hop" in meta["album"]
    assert isinstance(meta["youtube_tags"], list)
    assert Brand.DISTRIBUTOR in meta["streaming_description"]


def test_song_metadata_isrc_format():
    seo = SEOEngine()
    meta = seo.song_metadata("Test Track", "Afro House", bpm=124, sequence=42)
    assert meta["isrc"] == "CO-IMM-26-00042"


def test_suggest_song_names_chill():
    seo = SEOEngine()
    names = seo.suggest_song_names("Chill Hop", n=5)
    assert len(names) == 5
    assert all(isinstance(n, str) and len(n) > 3 for n in names)


def test_suggest_song_names_afro():
    seo = SEOEngine()
    names = seo.suggest_song_names("Afro House", n=3)
    assert len(names) == 3


def test_media_filename_format():
    seo = SEOEngine()
    fn = seo.media_filename("Galaxia Profunda", "thumbnail", "png")
    assert fn == "galaxia-profunda-thumbnail-immusic.png"
    assert " " not in fn
