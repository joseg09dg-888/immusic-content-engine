from unittest.mock import MagicMock, patch
from src.content_engine.writer import ContentWriter, PublicationPackage


def _mock_client(text: str):
    client = MagicMock()
    msg = MagicMock()
    msg.content = [MagicMock(text=text)]
    client.messages.create.return_value = msg
    return client


_FAKE_RESPONSE = """
SCRIPT:
Este es el guión completo en español para YouTube aplicando REBEL BRAIN METHOD.

CAPTIONS_INSTAGRAM:
Caption para Instagram con hashtags #RebelLuxury #IMMusic #Neurociencia

CAPTION_TIKTOK:
Hook viral para TikTok #IMMusic #RebelLuxury

YOUTUBE_TITLES:
1. Primer título optimizado para SEO
2. Segundo título variante con keywords
3. Tercer título alternativo engagement

YOUTUBE_DESCRIPTION:
Descripción completa con timestamps y keywords para YouTube.
"""

_BRIEF = {
    "titulo_principal": "How dopamine shapes music taste",
    "angulo_neurociencia": "Dopamine reward loop",
    "hook_apertura": "¿Sabías que tu cerebro elige música antes de que tú lo hagas?",
    "datos_clave": ["88% of listeners choose music based on mood"],
    "controversia": "Los algoritmos conocen tu cerebro mejor que tú",
    "fuentes": [{"source": "MBW", "url": "https://mbw.com"}],
}


def test_publication_package_structure():
    pkg = PublicationPackage(
        brief=_BRIEF,
        script_es="Guión en español...",
        captions_instagram="Caption IG...",
        caption_tiktok="Caption TK",
        youtube_titles=["Título 1", "Título 2", "Título 3"],
        youtube_description="Descripción YT...",
    )
    assert pkg.script_es.startswith("Guión")
    assert len(pkg.youtube_titles) == 3


def test_writer_generates_script():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_client(_FAKE_RESPONSE)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(_BRIEF)
    assert len(pkg.script_es) > 5
    assert len(pkg.captions_instagram) > 5
    assert len(pkg.youtube_titles) == 3


def test_writer_parses_youtube_titles():
    with patch("src.content_engine.writer.anthropic.Anthropic") as MockAnthropic:
        MockAnthropic.return_value = _mock_client(_FAKE_RESPONSE)
        writer = ContentWriter(api_key="fake-key")
        pkg = writer.generate(_BRIEF)
    assert pkg.youtube_titles[0] == "Primer título optimizado para SEO"
    assert pkg.youtube_titles[1] == "Segundo título variante con keywords"
    assert pkg.youtube_titles[2] == "Tercer título alternativo engagement"
