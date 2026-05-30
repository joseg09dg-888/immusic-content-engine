from unittest.mock import MagicMock, patch
from src.content_engine.writer import ContentWriter, PublicationPackage, CarouselSlide, _parse_carousel, _numbered_lines

_BRIEF = {
    "titulo_principal": "How dopamine shapes music taste",
    "angulo_neurociencia": "Dopamine reward loop",
    "hook_apertura": "¿Sabías que tu cerebro elige música antes de que tú lo hagas?",
    "datos_clave": ["88% of listeners choose music based on mood"],
    "controversia": "Los algoritmos conocen tu cerebro mejor que tú",
    "fuentes": [{"source": "MBW", "url": "https://mbw.com"}],
}

_FAKE_RESPONSE = """
SCRIPT_YOUTUBE:
Guión completo de YouTube aplicando REBEL BRAIN METHOD. Este es el contenido de más de 900 palabras para el video de YouTube. Neurociencia aplicada. Pattern Interrupt al inicio.

SCRIPT_SHORT:
Short de YouTube 55-58 segundos. Hook directo. Rebel Reframe al final.

SCRIPT_INSTAGRAM_REEL:
Reel de Instagram 7-45 segundos. Urbano. Directo.

SCRIPT_TIKTOK:
TikTok 21-90 segundos. Calle con datos. Hook que rompe el scroll.

SCRIPT_FACEBOOK_REEL:
Facebook Reel 30-60 segundos. Tono profesional-urbano.

CAROUSEL:
SLIDE 1:
El dato que la industria te oculta
Neurociencia aplicada al marketing musical.
SLIDE 2:
¿Por qué el 70% falla?
Sin estrategia personalizada, sin resultados.
SLIDE 3:
El cerebro decide antes que tú
Biología del consumidor musical explicada.
SLIDE 4:
REBEL LUXURY no es un look
Es un modelo de negocio.
SLIDE 5:
Medellín al mundo
La estrategia que nadie más aplica así.
SLIDE 6:
Chill Hop y Afro House
Géneros con propósito y posicionamiento.
SLIDE 7:
Tokenización musical
El futuro de las regalías ya llegó.
SLIDE 8:
El que entiende esto tiene ventaja
IM Music — donde la música se gestiona con técnica.

CAPTION_YOUTUBE:
El neuromarketing que la industria usa en silencio. Descúbrelo.

CAPTION_INSTAGRAM:
Caption completo para Instagram con voz REBEL LUXURY y hashtags #IMMusic #RebelLuxury #LujoRebelde

CAPTION_TIKTOK:
Cómo el cerebro elige música antes que tú #IMMusic #RebelLuxury #lofi

CAPTION_FACEBOOK:
Neurociencia aplicada a tu carrera musical. Así lo hace IM Music. #IMMusic

YOUTUBE_TITLES:
1. Neurociencia Musical — lo que la industria no te dice
2. Dopamina y Música — el método que cambia todo
3. Marketing Musical — neurociencia aplicada a tu carrera

YOUTUBE_DESCRIPTION:
Neurociencia aplicada a la industria musical — IM Music | REBEL LUXURY.
Descubre cómo el cerebro procesa la música y cómo los sellos lo usan en silencio.
00:00 Intro
02:30 El dato que cambia todo
05:00 Aplicación práctica
"""


def _mock_client(text: str):
    client = MagicMock()
    msg = MagicMock()
    msg.content = [MagicMock(text=text)]
    client.messages.create.return_value = msg
    return client


def test_publication_package_has_all_fields():
    pkg = PublicationPackage(brief=_BRIEF, script_es="Script aquí.")
    assert pkg.script_es == "Script aquí."
    assert pkg.script_short == ""
    assert pkg.carousel_slides == []
    assert pkg.youtube_titles == []


def test_parse_carousel_correct_count():
    text = """
SLIDE 1:
Título uno
Cuerpo uno
SLIDE 2:
Título dos
Cuerpo dos
SLIDE 3:
Título tres
Cuerpo tres
"""
    slides = _parse_carousel(text)
    assert len(slides) == 3
    assert slides[0].number == 1
    assert slides[0].title == "Título uno"
    assert "Cuerpo uno" in slides[0].body


def test_parse_carousel_caps_at_10():
    text = "\n".join(f"SLIDE {i}:\nTítulo {i}\nCuerpo {i}" for i in range(1, 15))
    slides = _parse_carousel(text)
    assert len(slides) == 10


def test_numbered_lines_extracts_3():
    text = "1. Primer título\n2. Segundo título\n3. Tercer título"
    lines = _numbered_lines(text, 3)
    assert lines[0] == "Primer título"
    assert lines[1] == "Segundo título"
    assert lines[2] == "Tercer título"


def test_numbered_lines_pads_to_n():
    text = "1. Solo uno"
    lines = _numbered_lines(text, 3)
    assert len(lines) == 3
    assert lines[1] == ""


def test_writer_generates_all_formats():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_client(_FAKE_RESPONSE)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(_BRIEF)
    assert len(pkg.script_es) > 10
    assert len(pkg.script_short) > 5
    assert len(pkg.script_instagram_reel) > 5
    assert len(pkg.script_tiktok) > 5
    assert len(pkg.script_facebook_reel) > 5


def test_writer_parses_carousel():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_client(_FAKE_RESPONSE)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(_BRIEF)
    assert len(pkg.carousel_slides) == 8
    assert pkg.carousel_slides[0].title == "El dato que la industria te oculta"
    assert pkg.carousel_slides[-1].number == 8


def test_writer_parses_youtube_titles():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_client(_FAKE_RESPONSE)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(_BRIEF)
    assert pkg.youtube_titles[0] == "Neurociencia Musical — lo que la industria no te dice"
    assert len(pkg.youtube_titles) == 3


def test_writer_parses_all_captions():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_client(_FAKE_RESPONSE)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(_BRIEF)
    assert "#IMMusic" in pkg.captions_instagram
    assert "#IMMusic" in pkg.caption_tiktok
    assert "#IMMusic" in pkg.caption_facebook
    assert len(pkg.caption_youtube) > 5


def test_writer_uses_cache_control():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        mock_client = _mock_client(_FAKE_RESPONSE)
        MockAnthropic.return_value = mock_client
        writer = ContentWriter(api_key="fake-key")
        writer.generate(_BRIEF)
    call_kwargs = mock_client.messages.create.call_args
    system = call_kwargs.kwargs.get("system") or call_kwargs[1].get("system")
    assert system[0]["cache_control"]["type"] == "ephemeral"
