from src.core.brand import Brand, Dimensions, Character, ContentDurations, RebelBrainMethod, VoiceProfile


def test_primary_colors():
    assert Brand.BLACK == "#000000"
    assert Brand.VIOLET == "#6200FF"
    assert Brand.WHITE == "#FFFFFF"


def test_concept():
    assert Brand.CONCEPT == "REBEL LUXURY"
    assert Brand.LABEL == "IM Music"
    assert Brand.HANDLE == "@immusicsello"


def test_dimensions_youtube_thumbnail():
    assert Dimensions.YOUTUBE_THUMBNAIL == (1280, 720)


def test_dimensions_instagram_square():
    assert Dimensions.INSTAGRAM_SQUARE == (1080, 1080)


def test_dimensions_instagram_story():
    assert Dimensions.INSTAGRAM_STORY == (1080, 1920)


def test_dimensions_tiktok_cover():
    assert Dimensions.TIKTOK_COVER == (1080, 1920)


def test_cover_art_size():
    assert Dimensions.COVER_ART == (3000, 3000)


def test_characters():
    assert Character.CHILL_HOP.name == "El Viajero Nocturno"
    assert Character.CHILL_HOP.genre == "Chill Hop"
    assert Character.CHILL_HOP.bpm_range == (85, 95)
    assert Character.AFRO_HOUSE.name == "El Ser Galáctico"
    assert Character.AFRO_HOUSE.genre == "Afro House"
    assert Character.AFRO_HOUSE.bpm_range == (120, 128)


def test_lufs_targets():
    assert Brand.LUFS_SPOTIFY == -14
    assert Brand.LUFS_YOUTUBE == -13
    assert Brand.LUFS_APPLE == -16


def test_publish_days():
    assert Brand.PUBLISH_DAYS == ["Monday", "Wednesday", "Friday"]


def test_publish_times():
    assert Brand.PUBLISH_TIMES == {"youtube": "18:00", "instagram": "19:00", "tiktok": "20:00"}


def test_color_palette_completeness():
    palette = Brand.palette()
    assert "black" in palette
    assert "violet" in palette
    assert "white" in palette
    assert all(v.startswith("#") for v in palette.values())


def test_content_durations_song():
    assert ContentDurations.SONG_MAX == 170
    assert ContentDurations.SONG_FADE_START == 155
    assert ContentDurations.SONG_FADE_START < ContentDurations.SONG_MAX


def test_content_durations_youtube():
    assert ContentDurations.YOUTUBE_MIN == 480
    assert ContentDurations.YOUTUBE_MAX == 900
    assert ContentDurations.YOUTUBE_SHORT_MIN == 55
    assert ContentDurations.YOUTUBE_SHORT_MAX == 58


def test_content_durations_social():
    assert ContentDurations.TIKTOK_MIN == 21
    assert ContentDurations.TIKTOK_MAX == 90
    assert ContentDurations.INSTAGRAM_REEL_MIN == 7
    assert ContentDurations.INSTAGRAM_REEL_MAX == 45


def test_rebel_brain_method_steps():
    assert len(RebelBrainMethod.STEPS) == 5
    assert RebelBrainMethod.STEPS[0] == "Pattern Interrupt"
    assert RebelBrainMethod.STEPS[-1] == "Rebel Reframe"


def test_rebel_brain_method_prompt_block():
    block = RebelBrainMethod.as_prompt_block()
    assert "PATTERN INTERRUPT" in block
    assert "TENSION BUILDER" in block
    assert "CREDIBILITY ANCHOR" in block
    assert "INSIGHT REVELATION" in block
    assert "REBEL REFRAME" in block


def test_voice_profile_motor():
    assert "Respeto" in VoiceProfile.MOTOR


def test_voice_profile_tagline():
    assert VoiceProfile.TAGLINE == "Lujo Rebelde"


def test_voice_profile_ceo_traits():
    assert len(VoiceProfile.CEO_TRAITS) == 3
    assert "Original" in VoiceProfile.CEO_TRAITS
    assert "Directo" in VoiceProfile.CEO_TRAITS


def test_voice_profile_audience_keys():
    assert "primary" in VoiceProfile.AUDIENCE
    assert "secondary" in VoiceProfile.AUDIENCE
    assert "geo" in VoiceProfile.AUDIENCE
    assert "Medellín" in VoiceProfile.AUDIENCE["geo"]


def test_voice_profile_words_no_includes_key_terms():
    assert "síguenos" in VoiceProfile.WORDS_NO
    assert "somos los mejores" in VoiceProfile.WORDS_NO


def test_voice_profile_prompt_block_has_voice():
    block = VoiceProfile.as_prompt_block()
    assert Brand.LABEL in block
    assert "Respeto" in block
    assert "NUNCA" in block
