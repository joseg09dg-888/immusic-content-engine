from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class _Character:
    name: str
    genre: str
    bpm_range: Tuple[int, int]
    scene: str


class Character:
    CHILL_HOP = _Character(
        name="El Viajero Nocturno",
        genre="Chill Hop",
        bpm_range=(85, 95),
        scene="Ciudad nocturna futurista, lluvia suave, neón violeta, constelaciones",
    )
    AFRO_HOUSE = _Character(
        name="El Ser Galáctico",
        genre="Afro House",
        bpm_range=(120, 128),
        scene="Galaxia abierta, nebulosas, polvo estelar que vibra con el beat",
    )


class Dimensions:
    YOUTUBE_THUMBNAIL: Tuple[int, int] = (1280, 720)
    INSTAGRAM_SQUARE: Tuple[int, int] = (1080, 1080)
    INSTAGRAM_STORY: Tuple[int, int] = (1080, 1920)
    TIKTOK_COVER: Tuple[int, int] = (1080, 1920)
    COVER_ART: Tuple[int, int] = (3000, 3000)
    YOUTUBE_VIDEO: Tuple[int, int] = (1920, 1080)


class ContentDurations:
    """Target durations in seconds for each platform/format."""
    YOUTUBE_MIN: int = 480
    YOUTUBE_MAX: int = 900
    YOUTUBE_SHORT_MIN: int = 55
    YOUTUBE_SHORT_MAX: int = 58
    INSTAGRAM_REEL_MIN: int = 7
    INSTAGRAM_REEL_MAX: int = 45
    INSTAGRAM_CAROUSEL_SLIDES: Tuple[int, int] = (8, 10)
    TIKTOK_MIN: int = 21
    TIKTOK_MAX: int = 90
    FACEBOOK_REEL_MIN: int = 30
    FACEBOOK_REEL_MAX: int = 60
    SONG_MAX: int = 170
    SONG_FADE_START: int = 155


class RebelBrainMethod:
    """
    REBEL BRAIN METHOD — framework obligatorio en cada pieza.
    Voz: autoridad + rebeldía intelectual + lujo de conocimiento. Sin venta directa.
    """
    STEPS = [
        "Pattern Interrupt",
        "Tension Builder",
        "Credibility Anchor",
        "Insight Revelation",
        "Rebel Reframe",
    ]

    PATTERN_INTERRUPT = (
        "Rompe el patrón de atención en los primeros 5 segundos. "
        "Dato contraintuitivo, pregunta que desafía, o afirmación que contradice lo obvio."
    )
    TENSION_BUILDER = (
        "Construye tensión con una paradoja o problema sin resolver. "
        "El oyente debe sentir que le falta información crítica."
    )
    CREDIBILITY_ANCHOR = (
        "Anclaje de credibilidad: dato científico, estadística, estudio real, o caso documentado. "
        "No inventar números. Citar fuente siempre."
    )
    INSIGHT_REVELATION = (
        "La revelación: la conexión que nadie más ha hecho entre neurociencia y la industria musical. "
        "Ángulo único de IM Music / REBEL LUXURY."
    )
    REBEL_REFRAME = (
        "Reencuadre rebelde: cuestiona lo establecido sin atacar personas. "
        "CTA implícito de identidad IM Music. Sin llamados directos a comprar."
    )

    @classmethod
    def as_prompt_block(cls) -> str:
        return (
            "REBEL BRAIN METHOD — aplica este framework en orden:\n"
            f"1. PATTERN INTERRUPT: {cls.PATTERN_INTERRUPT}\n"
            f"2. TENSION BUILDER: {cls.TENSION_BUILDER}\n"
            f"3. CREDIBILITY ANCHOR: {cls.CREDIBILITY_ANCHOR}\n"
            f"4. INSIGHT REVELATION: {cls.INSIGHT_REVELATION}\n"
            f"5. REBEL REFRAME: {cls.REBEL_REFRAME}\n"
        )


class Brand:
    BLACK: str = "#000000"
    VIOLET: str = "#6200FF"
    WHITE: str = "#FFFFFF"

    CONCEPT: str = "REBEL LUXURY"
    LABEL: str = "IM Music"
    HANDLE: str = "@immusicsello"
    MOTIFS: list = ["constelaciones", "galaxia", "líneas de luz", "polvo estelar"]

    LUFS_SPOTIFY: int = -14
    LUFS_YOUTUBE: int = -13
    LUFS_APPLE: int = -16

    PUBLISH_DAYS: list = ["Monday", "Wednesday", "Friday"]
    PUBLISH_TIMES: dict = {
        "youtube": "18:00",
        "instagram": "19:00",
        "tiktok": "20:00",
    }

    DISTRIBUTOR: str = "Nexus"
    DISTRIBUTOR_CUT: float = 0.08

    @classmethod
    def palette(cls) -> dict:
        return {
            "black": cls.BLACK,
            "violet": cls.VIOLET,
            "white": cls.WHITE,
        }
