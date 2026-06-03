import re
from typing import List, Optional
from src.core.brand import Brand, VoiceProfile, Character

# Keyword pools — research-based, not invented
_CHILL_HOP_KW = [
    "chill hop", "lofi", "lo-fi hip hop", "study music", "focus music",
    "work music", "relax music", "beats to study", "chill beats",
    "lofi jazz", "jazzy hip hop", "instrumental hip hop", "musica para estudiar",
    "musica para trabajar", "musica para concentrarse", "lofi chill",
]
_AFRO_HOUSE_KW = [
    "afro house", "deep house", "afrobeats", "african house",
    "deep afro house", "melodic house", "organic house", "tribal house",
    "afrobeat instrumental", "house music", "deep afro",
]
_GENERAL_KW = [
    "IM Music", "REBEL LUXURY", "musica colombiana", "latin beats",
    "latin music instrumental", "sello discografico colombia", "musica latina",
    "new music 2026", "colombian music",
]
_MARKETING_KW = [
    "marketing musical", "industria musical", "neuromarketing",
    "psicologia del marketing", "estrategia digital musica",
    "marketing para artistas", "music business", "industria de la musica",
    "neurociencia del consumidor", "comportamiento del consumidor",
    "estrategia de marca", "branding musical", "marketing de contenidos",
]
_IG_BIG = ["#music", "#marketing", "#spotify", "#newmusic", "#lofi", "#hiphop"]
_IG_MEDIUM = [
    "#chillhop", "#afrohouse", "#musicbusiness", "#marketingdigital",
    "#neuromarketing", "#musicmarketing", "#latinmusic", "#estudia",
    "#lofibeats", "#deephouse",
]
_IG_NICHE = [
    "#IMMusic", "#RebelLuxury", "#LujoRebelde", "#SelladoIMMusic",
    "#artistaemergente", "#musicacolombiana", "#medellinmusic",
    "#strategiamusical", "#psicologiademarketing",
]
_TT_TAGS = [
    "#immusic", "#rebeluxury", "#marketing", "#musica", "#lofi",
    "#neuromarketing", "#afrohouse", "#chillhop", "#musicbusiness",
]

# Song naming pools — REBEL LUXURY aesthetic, NOT generic
_CHILL_HOP_NAMES = [
    "Galaxia Profunda", "Hora Azul", "Polvo Estelar", "Arquitectura del Silencio",
    "Lluvia de Neón", "Ciudad Invisible", "Órbita Suave", "Luz de Madrugada",
    "Constelación", "Viaje Nocturno", "Eclipse Lento", "Atmósfera Índigo",
    "Mar de Cuarzo", "Terraza Infinita", "Deriva Cósmica", "Niebla Eléctrica",
]
_AFRO_HOUSE_NAMES = [
    "Cosmos Afro", "Pulso Galáctico", "Tierra y Estrella", "Ritual del Vacío",
    "Frecuencia Negra", "Nebulosa Tribal", "Danza del Universo", "Portal Oscuro",
    "Espiral Profunda", "Energía Primordial", "Vórtice Afro", "Rugido Estelar",
    "Latido Cósmico", "Horizonte Tribal", "Sombra Luminosa", "Campo Magnético",
]


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def _fit(title: str, promise: str, max_len: int) -> str:
    full = f"{title} — {promise}"
    if len(full) <= max_len:
        return full
    if len(title) >= max_len:
        return title[:max_len]
    available = max_len - len(title) - 4
    if available <= 0:
        return title[:max_len]
    return f"{title} — {promise[:available].rstrip()}"


class SEOEngine:
    """Generates SEO metadata for all platforms. No API calls — pure keyword logic."""

    # ── YouTube ──────────────────────────────────────────────────────────────

    def youtube_titles(self, keyword: str, topic: str) -> List[str]:
        """3 title variants: [Keyword] — [Rebel Luxury promise], max 60 chars."""
        promises = [
            f"lo que la industria no te dice",
            f"neurociencia aplicada a tu carrera",
            f"el método que cambia todo",
        ]
        return [_fit(keyword[:35], p, 60) for p in promises]

    def youtube_tags(self, topic: str, genre: str = "") -> List[str]:
        """15-20 tags: broad + specific + long-tail."""
        base = _MARKETING_KW[:6] + _GENERAL_KW[:4]
        if "chill" in genre.lower():
            base += _CHILL_HOP_KW[:5]
        elif "afro" in genre.lower():
            base += _AFRO_HOUSE_KW[:5]
        topic_words = [w for w in topic.lower().split() if len(w) > 4][:3]
        return list(dict.fromkeys(base + topic_words))[:20]

    def youtube_channel_tags(self) -> str:
        """Channel-level tags string, max 500 chars."""
        tags = (
            _GENERAL_KW + _MARKETING_KW[:8] + _CHILL_HOP_KW[:5] + _AFRO_HOUSE_KW[:5]
        )
        result = ", ".join(tags)
        return result[:500]

    def youtube_channel_description(self) -> str:
        return (
            f"{Brand.LABEL} — {VoiceProfile.TAGLINE}. "
            "Sello discográfico y agencia de marketing musical en Medellín, Colombia. "
            "Psicología aplicada a la industria musical. "
            "Contenido de neurociencia del marketing, estrategia musical, y beats originales. "
            "Géneros: Chill Hop · Afro House. "
            f"Distribución global vía Nexus. Plataforma: {Brand.HANDLE}"
        )

    # ── Instagram ─────────────────────────────────────────────────────────────

    def instagram_hashtags(self, topic: str = "", genre: str = "") -> str:
        """3-5 big + 5-8 medium + 5-7 niche. Topic-aware."""
        big = _IG_BIG[:4]
        medium = _IG_MEDIUM[:7]
        niche = _IG_NICHE[:6]
        if genre:
            g = genre.lower()
            if "chill" in g:
                medium.append("#chillhop")
            elif "afro" in g:
                medium.append("#afrohouse")
        all_tags = list(dict.fromkeys(big + medium + niche))
        return " ".join(all_tags[:18])

    def instagram_bio(self) -> str:
        return (
            f"🎵 {Brand.LABEL} | {VoiceProfile.TAGLINE}\n"
            "Sello · Marketing Musical · Neurociencia\n"
            "Medellín 🇨🇴 → Mundo\n"
            "Chill Hop · Afro House\n"
            "👇 Plataforma para artistas"
        )

    # ── TikTok ────────────────────────────────────────────────────────────────

    def tiktok_hashtags(self, genre: str = "") -> str:
        tags = _TT_TAGS[:5]
        if "chill" in genre.lower():
            tags.append("#lofi")
        elif "afro" in genre.lower():
            tags.append("#afrohouse")
        return " ".join(tags)

    def tiktok_bio(self) -> str:
        return f"{Brand.LABEL} | {VoiceProfile.TAGLINE} 🎵 Medellín→Mundo · Chill Hop · Afro House"

    # ── Song metadata ─────────────────────────────────────────────────────────

    def song_metadata(
        self, track_name: str, genre: str, bpm: int, sequence: int = 1, year: int = 2026
    ) -> dict:
        isrc = f"CO-IMM-{str(year)[2:]}-{sequence:05d}"
        kw = _CHILL_HOP_KW[:6] if "chill" in genre.lower() else _AFRO_HOUSE_KW[:6]
        streaming_desc = (
            f"{track_name} — {Brand.LABEL} | {Brand.CONCEPT}. "
            f"Genre: {genre}. BPM: {bpm}. "
            + ", ".join(kw[:4])
            + ". "
            "Perfect for studying, working, or deep focus. "
            f"© {Brand.LABEL} {year}. Distributed by {Brand.DISTRIBUTOR}."
        )
        return {
            "title": track_name,
            "artist": Brand.LABEL,
            "album": f"{Brand.LABEL} — {genre} Sessions {year}",
            "genre": genre,
            "bpm": bpm,
            "year": year,
            "label": f"{Brand.LABEL} Records",
            "isrc": isrc,
            "copyright": f"© {Brand.LABEL} {year}",
            "streaming_description": streaming_desc,
            "youtube_tags": self.youtube_tags(track_name, genre),
            "spotify_genres": kw[:4],
        }

    def youtube_monetization_seo(
        self, title: str, brief: dict, duration_sec: int = 480
    ) -> dict:
        """Full monetization-ready SEO package for a YouTube video."""
        _STOPWORDS = {"de", "la", "el", "en", "un", "una", "los", "las", "que", "y", "a", "con", "del"}
        raw_text = title + " " + brief.get("angulo_neurociencia", "")
        words = [w.lower().strip(".,;:!?") for w in raw_text.split()]
        keywords = list(dict.fromkeys(
            w for w in words if len(w) > 4 and w not in _STOPWORDS
        ))[:5]

        keyword_principal = keywords[0] if keywords else title.split()[0].lower()
        titulo_optimizado = f"{keyword_principal} — {title}"[:70]

        # Generate chapters based on duration
        n_chapters = max(5, duration_sec // 90)
        interval = duration_sec // n_chapters
        chapter_labels = [
            "Introducción",
            "El dato que nadie menciona",
            "La neurociencia detrás",
            "El método REBEL LUXURY",
            "Conclusión",
        ]
        # Extend with generic labels if more chapters needed
        extras = [f"Punto {i+1}" for i in range(5, n_chapters)]
        all_labels = chapter_labels + extras

        capitulos = []
        for idx in range(n_chapters):
            t = idx * interval
            minutes = t // 60
            seconds = t % 60
            label = all_labels[idx] if idx < len(all_labels) else f"Sección {idx+1}"
            capitulos.append({"tiempo": f"{minutes}:{seconds:02d}", "titulo": label})

        tags_prioritarios = [keyword_principal] + keywords[1:] + [
            "marketing musical", "IM Music", "REBEL LUXURY"
        ]
        tags_longtail = [
            f"{keyword_principal} para artistas",
            "marketing musical 2026",
            "IM Music",
            "neurociencia musical",
            f"{keyword_principal} industria musical",
            "estrategia para artistas",
            "REBEL LUXURY método",
            "music business colombia",
        ]

        watch_time_target_min = round(duration_sec * 0.55 / 60, 1)
        meta_description = (
            f"{titulo_optimizado}. {brief.get('angulo_neurociencia', '')} "
            f"IM Music — REBEL LUXURY. {', '.join(tags_prioritarios[:4])}."
        )[:160]

        return {
            "titulo_optimizado": titulo_optimizado,
            "tags_prioritarios": list(dict.fromkeys(tags_prioritarios))[:10],
            "tags_longtail": tags_longtail,
            "capitulos": capitulos,
            "watch_time_target_min": watch_time_target_min,
            "keyword_principal": keyword_principal,
            "meta_description": meta_description,
        }

    def tiktok_seo_complete(self, title: str, brief: dict) -> dict:
        """Complete TikTok SEO package: caption, hashtags, sounds, schedule."""
        viral_tags  = ["#fyp", "#parati", "#foryou", "#viral2026"]
        niche_tags  = ["#musicaindustria", "#marketingmusical", "#artistas", "#rebelluxury", "#immusic"]
        brand_tags  = ["#IMMusic", "#REBELLuxury"]

        hashtags_completos    = viral_tags + niche_tags + brand_tags
        hashtags_prioritarios = viral_tags + brand_tags

        hook = brief.get("hook", title)
        all_tags_str = " ".join(hashtags_completos[:8])
        caption_raw  = hook[:80] + " " + all_tags_str
        caption_150chars = caption_raw[:150]

        sonidos_sugeridos = [
            "trending audio — verificar en FYP actual",
            "beat lofi/chillhop — biblioteca TikTok",
            "audio original IM Music — REBEL LUXURY",
        ]

        return {
            "caption_150chars": caption_150chars,
            "hashtags_completos": hashtags_completos,
            "hashtags_prioritarios": hashtags_prioritarios,
            "sonidos_sugeridos": sonidos_sugeridos,
            "horario_optimo": "20:00 hora Colombia (L/M/V)",
            "duracion_optima_seg": 45,
        }

    def suggest_song_names(self, genre: str, n: int = 5) -> List[str]:
        """Returns n name suggestions following REBEL LUXURY naming convention."""
        pool = _CHILL_HOP_NAMES if "chill" in genre.lower() else _AFRO_HOUSE_NAMES
        return pool[:n]

    # ── File naming ───────────────────────────────────────────────────────────

    def media_filename(self, track_name: str, format_: str, ext: str) -> str:
        """SEO-friendly filename before upload: keyword-description-immusic.ext"""
        return f"{_slug(track_name)}-{_slug(format_)}-immusic.{ext}"
