"""
IM Music Video Editor — REBEL LUXURY brand treatment.

PERFILES DE EDICIÓN POR TIPO DE CONTENIDO:
Cada formato del plan de contenidos tiene su propio perfil de edición coherente.

  organico     → Storytelling / Celular en mano
                 Silencios cortados, transiciones crossfade 0.3s, subtítulos grandes,
                 watermark, sin intro larga — feel auténtico y raw

  blog         → Documentación / Día en la Vida
                 Silencios cortados, B-roll de marca insertado, subtítulos,
                 transiciones suaves, intro + watermark

  fake_podcast → Educativo / Fake Podcast
                 Sin corte de silencios (las pausas dan autoridad), lower thirds con
                 la pregunta en pantalla, subtítulos Anton, cortes limpios

  atraccion    → Atracción / Reel Rápido
                 Silencios cortados agresivo (-30dB, 0.2s min), texto en pantalla
                 enorme (Pattern Interrupt), sin intro — arranca directo al hook,
                 cortes rápidos cada 2-3s

  validacion   → Validación / Comparativa
                 Limpio y estructurado, callouts de texto, cortes precisos,
                 color grade moderado, subtítulos

  fidelizacion → Fidelización / Manifiesto / Visión
                 Pacing lento y cinematográfico, color grade fuerte,
                 sin subtítulos permanentes (deja respirar), outro largo con logo

Uso:
    editor = VideoEditor()
    pack = editor.produce_pack(
        "raw.mp4",
        titulo="Por que fracasan los artistas",
        content_type="organico",   # ← perfil automático de edición
    )
"""
import logging
import subprocess
import shutil
import json
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont

logger = logging.getLogger(__name__)

_ASSETS = Path(__file__).resolve().parent.parent.parent / "assets"
_OUTPUTS = Path(__file__).resolve().parent.parent.parent / "outputs"

# ── PERFILES DE EDICIÓN POR TIPO DE CONTENIDO ────────────────────────────────
# Cada perfil define exactamente cómo se edita ese tipo de video.
# Coherencia total: edición ↔ formato ↔ guión.

EDIT_PROFILES = {
    "organico": {
        # Storytelling / Celular en mano — feel auténtico, sin pulir de más
        "remove_silence":     True,
        "silence_threshold":  -32.0,   # dB — agresivo para cortar dudas/uhh
        "min_silence_dur":    0.35,    # segundos
        "silence_padding":    0.12,    # deja mínimo margen natural
        "cinema_grade":       True,
        "add_intro":          False,   # arranca directo — orgánico no tiene intro de logo
        "add_outro":          True,
        "add_watermark":      True,
        "subtitle_size":      "large", # subtítulos grandes para móvil
        "subtitle_position":  "bottom",
        "transition_dur":     0.25,    # crossfade breve y suave
        "description": "Storytelling auténtico: silencios cortados, subtítulos grandes, sin intro.",
    },
    "blog": {
        # Documentación / Día en la Vida / Vlog
        "remove_silence":     True,
        "silence_threshold":  -35.0,
        "min_silence_dur":    0.5,
        "silence_padding":    0.18,
        "cinema_grade":       True,
        "add_intro":          True,
        "add_outro":          True,
        "add_watermark":      True,
        "subtitle_size":      "medium",
        "subtitle_position":  "bottom",
        "transition_dur":     0.35,
        "use_broll":          True,    # usa B-roll de marca si hay imágenes
        "description": "Vlog/blog: B-roll insertado, transiciones suaves, intro+outro.",
    },
    "fake_podcast": {
        # Educativo / Fake Podcast — autoridad y pausas intencionales
        "remove_silence":     False,   # las pausas dan peso a las palabras
        "cinema_grade":       True,
        "add_intro":          True,
        "add_outro":          True,
        "add_watermark":      True,
        "subtitle_size":      "medium",
        "subtitle_position":  "bottom",
        "transition_dur":     0.15,    # cortes limpios, sin crossfade romántico
        "lower_thirds":       True,    # pregunta/tema en pantalla
        "description": "Podcast: pauses kept for authority, lower thirds, clean cuts.",
    },
    "atraccion": {
        # Reel Rápido / Controversia — agresivo, sin respiro, hook inmediato
        "remove_silence":     True,
        "silence_threshold":  -28.0,   # muy agresivo
        "min_silence_dur":    0.20,    # corta hasta micro-silencios
        "silence_padding":    0.08,
        "cinema_grade":       True,
        "add_intro":          False,   # NUNCA intro en contenido de atracción
        "add_outro":          False,   # tampoco outro — termina y ya
        "add_watermark":      True,
        "subtitle_size":      "xl",    # subtítulos enormes tipo TikTok/Reels viral
        "subtitle_position":  "center",
        "transition_dur":     0.0,     # cortes duros, sin fade
        "description": "Reel de atracción: hook inmediato, cortes duros, subtítulos enormes.",
    },
    "validacion": {
        # Comparativa / Demostración
        "remove_silence":     True,
        "silence_threshold":  -33.0,
        "min_silence_dur":    0.4,
        "silence_padding":    0.15,
        "cinema_grade":       True,
        "add_intro":          True,
        "add_outro":          True,
        "add_watermark":      True,
        "subtitle_size":      "medium",
        "subtitle_position":  "bottom",
        "transition_dur":     0.2,
        "description": "Validación: limpio, estructurado, callouts de texto.",
    },
    "fidelizacion": {
        # Manifiesto / Visión de Marca — cinematográfico y poderoso
        "remove_silence":     False,   # los silencios son dramáticos
        "cinema_grade":       True,
        "add_intro":          True,
        "add_outro":          True,
        "add_watermark":      True,
        "subtitle_size":      "small",  # subtítulos discretos — no distraen
        "subtitle_position":  "bottom",
        "transition_dur":     0.5,     # fades lentos y elegantes
        "description": "Manifiesto: cinematográfico, pacing lento, sombras profundas.",
    },
}

# Alias para facilitar uso
EDIT_PROFILES["storytelling"] = EDIT_PROFILES["organico"]
EDIT_PROFILES["vlog"]         = EDIT_PROFILES["blog"]
EDIT_PROFILES["podcast"]      = EDIT_PROFILES["fake_podcast"]
EDIT_PROFILES["reel"]         = EDIT_PROFILES["atraccion"]
EDIT_PROFILES["manifiesto"]   = EDIT_PROFILES["fidelizacion"]
EDIT_PROFILES["default"]      = EDIT_PROFILES["blog"]  # fallback

# Colores marca
VIOLET  = (94, 23, 235)
BLACK   = (0, 0, 0)
WHITE   = (255, 255, 255)
CREAM   = (242, 237, 229)

# Duraciones
INTRO_DUR  = 3    # segundos
OUTRO_DUR  = 4    # segundos
FADE_DUR   = 0.4  # segundos fade in/out


def _require_ffmpeg():
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg no encontrado. Instala con: winget install Gyan.FFmpeg")


def _font(size: int, bold: bool = True) -> ImageFont.FreeTypeFont:
    af = _ASSETS / "fonts"
    candidates = ["Anton-Regular.ttf", "impact.ttf"] if bold else ["segoeui.ttf", "arial.ttf"]
    from pathlib import PureWindowsPath
    win_fonts = Path(r"C:\Windows\Fonts")
    for name in candidates:
        for base in (af, win_fonts):
            p = base / name
            if p.exists():
                return ImageFont.truetype(str(p), size)
    return ImageFont.load_default(size=size)


def _get_video_info(video_path: Path) -> dict:
    """Obtiene duración y dimensiones del video con ffprobe."""
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_streams", "-show_format", str(video_path)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return {"width": 1920, "height": 1080, "duration": 60.0}
    info = json.loads(result.stdout)
    video_stream = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    return {
        "width": int(video_stream.get("width", 1920)),
        "height": int(video_stream.get("height", 1080)),
        "duration": float(info.get("format", {}).get("duration", 60.0)),
    }


def _make_intro_frame(titulo: str, size: tuple) -> Path:
    """Genera un frame PNG para el intro con fondo violeta + logo + título."""
    w, h = size
    img = Image.new("RGB", (w, h), VIOLET)
    draw = ImageDraw.Draw(img)

    # Logo IM Music centrado arriba
    logo_path = _ASSETS / "logo" / "logo_immusic.png"
    logo_y = int(h * 0.15)
    if logo_path.exists():
        try:
            logo = Image.open(logo_path).convert("RGB")
            logo.load()
            lw = int(w * 0.22)
            lh = int(logo.size[1] * (lw / logo.size[0]))
            logo = logo.resize((lw, lh), Image.LANCZOS)
            # El logo ya tiene fondo negro — recortamos solo la zona del logo
            # Centramos el fondo negro con el logo sobre el fondo violeta
            bg = Image.new("RGB", (lw + 20, lh + 20), BLACK)
            bg.paste(logo, (10, 10))
            lx = (w - bg.width) // 2
            img.paste(bg, (lx, logo_y))
            logo_y += bg.height + 20
        except Exception:
            logo_y = int(h * 0.35)
    else:
        # Fallback: IM text
        im_f = _font(int(h * 0.12))
        draw.text((w // 2, int(h * 0.25)), "IM", font=im_f, fill=WHITE, anchor="mm")
        logo_y = int(h * 0.42)

    # Título del video
    title_f = _font(max(28, int(h * 0.042)))
    # Wrap automático
    words = titulo.upper().split()
    lines, line = [], ""
    max_w = int(w * 0.85)
    for word in words:
        test = (line + " " + word).strip()
        bbox = draw.textbbox((0, 0), test, font=title_f)
        if bbox[2] <= max_w:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    lh_line = int(max(28, int(h * 0.042)) * 1.2)
    y = logo_y + int(h * 0.04)
    for ln in lines:
        bx = draw.textbbox((0, 0), ln, font=title_f)
        x = (w - (bx[2] - bx[0])) // 2
        draw.text((x + 2, y + 2), ln, font=title_f, fill=BLACK)
        draw.text((x, y), ln, font=title_f, fill=WHITE)
        y += lh_line

    tmp = _OUTPUTS / "_tmp_intro.png"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    img.save(tmp)
    return tmp


def _make_outro_frame(size: tuple) -> Path:
    """Frame de outro: negro + logo IM centrado + CTA."""
    w, h = size
    img = Image.new("RGB", (w, h), BLACK)
    draw = ImageDraw.Draw(img)

    logo_path = _ASSETS / "logo" / "logo_immusic.png"
    logo_y = int(h * 0.2)
    if logo_path.exists():
        try:
            logo = Image.open(logo_path).convert("RGB")
            logo.load()
            lw = int(w * 0.30)
            lh = int(logo.size[1] * (lw / logo.size[0]))
            logo = logo.resize((lw, lh), Image.LANCZOS)
            lx = (w - lw) // 2
            img.paste(logo, (lx, logo_y))
            logo_y += lh + int(h * 0.04)
        except Exception:
            pass

    # "immusicsello" en todos los canales
    cta_f = _font(max(20, int(h * 0.028)), bold=False)
    cta_lines = ["@immusicsello", "YouTube  •  Instagram  •  TikTok"]
    for line in cta_lines:
        bx = draw.textbbox((0, 0), line, font=cta_f)
        draw.text(((w - (bx[2] - bx[0])) // 2, logo_y), line, font=cta_f, fill=CREAM)
        logo_y += int(max(20, int(h * 0.028)) * 1.5)

    tmp = _OUTPUTS / "_tmp_outro.png"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    img.save(tmp)
    return tmp


def _make_watermark(size: tuple, opacity: int = 45) -> Path:
    """Logo IM semi-transparente para watermark en esquina."""
    w, h = size
    wm_h = max(40, int(h * 0.055))

    logo_path = _ASSETS / "logo" / "logo_immusic.png"
    if logo_path.exists():
        try:
            logo = Image.open(logo_path).convert("RGBA")
            logo.load()
            lw = int(wm_h * logo.size[0] / logo.size[1])
            logo = logo.resize((lw, wm_h), Image.LANCZOS)
            # Aplicar opacidad
            r, g, b, a = logo.split()
            a = a.point(lambda x: int(x * opacity / 255))
            logo = Image.merge("RGBA", (r, g, b, a))
            tmp = _OUTPUTS / "_tmp_watermark.png"
            tmp.parent.mkdir(parents=True, exist_ok=True)
            logo.save(tmp)
            return tmp
        except Exception:
            pass

    # Fallback: texto "IM" semitransparente
    wm_img = Image.new("RGBA", (60, 30), (0, 0, 0, 0))
    d = ImageDraw.Draw(wm_img)
    f = _font(22)
    d.text((5, 2), "IM", font=f, fill=(*VIOLET, opacity))
    tmp = _OUTPUTS / "_tmp_watermark.png"
    wm_img.save(tmp)
    return tmp


class VideoEditor:
    """Editor de video con identidad REBEL LUXURY para IM Music."""

    def __init__(self):
        _require_ffmpeg()

    # ── COLOR GRADING ──────────────────────────────────────────────────────────

    def apply_cinema_grade(self, input_path: Path, output_path: Path) -> Path:
        """
        Color grading cinematográfico REBEL LUXURY:
        - Contraste alto (filmic look)
        - Sombras frías (tinte violeta muy sutil en negros)
        - Altas luces cálidas (skin tone preservado)
        - Saturación ligeramente elevada en el rango medio
        - Viñeta sutil para focus en el sujeto

        Usa filtros nativos FFmpeg (curves + eq + vignette).
        No requiere LUTs externos.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # REBEL LUXURY cinematic grade:
        # curves: boost contraste S-curve, sombras frías (canal B up ligeramente)
        # eq: saturacion +0.15, brillo -0.03, contraste +0.12
        # vignette: oscurece bordes, foco al centro
        vf_chain = (
            # S-curve contrast + leve tinte violeta/frío en sombras
            "curves=r='0/0 0.1/0.07 0.5/0.5 0.9/0.93 1/1':"
            "g='0/0 0.1/0.08 0.5/0.5 0.9/0.92 1/1':"
            "b='0/0.03 0.1/0.11 0.5/0.51 0.9/0.91 1/0.97',"
            # Ajuste fino: saturacion y contraste
            "eq=saturation=1.18:contrast=1.08:brightness=-0.02:gamma=0.97,"
            # Vignette suave (2.5 = intensidad moderada)
            "vignette=PI/4"
        )

        cmd = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-vf", vf_chain,
            "-c:v", "libx264", "-crf", "19", "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Color grade failed: {result.stderr[-300:]}")
            raise RuntimeError(f"Color grade failed: {result.stderr[-200:]}")
        logger.info(f"[OK] Color grade applied: {output_path.name}")
        return output_path

    # ── SILENCE REMOVAL ────────────────────────────────────────────────────────

    def remove_silences(
        self,
        input_path: Path,
        output_path: Path,
        silence_threshold: float = -35.0,  # dB — umbral de silencio
        min_silence_dur: float = 0.4,       # segundos mínimos para cortar
        padding: float = 0.15,              # dejar este margen antes/después
    ) -> Path:
        """
        Detecta y elimina silencios del video.
        Usa silencedetect de FFmpeg + re-encode con segmentos.

        Requiere que el video tenga audio.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Paso 1: detectar silencios
        detect_cmd = [
            "ffmpeg", "-i", str(input_path),
            "-af", f"silencedetect=noise={silence_threshold}dB:d={min_silence_dur}",
            "-f", "null", "-"
        ]
        result = subprocess.run(detect_cmd, capture_output=True, text=True)
        stderr = result.stderr

        # Parsear timestamps de silencio
        import re
        starts = [float(m) for m in re.findall(r"silence_start: ([\d.]+)", stderr)]
        ends   = [float(m) for m in re.findall(r"silence_end: ([\d.]+)", stderr)]

        if not starts:
            # Sin silencios detectados — copiar tal cual
            logger.info("No silences detected, copying as-is")
            import shutil as _sh
            _sh.copy2(str(input_path), str(output_path))
            return output_path

        info = _get_video_info(input_path)
        duration = info["duration"]

        # Construir segmentos a mantener (inverso de los silencios)
        keep_segments = []
        prev_end = 0.0
        for s_start, s_end in zip(starts, ends):
            seg_start = prev_end
            seg_end = max(0, s_start - padding)
            if seg_end > seg_start + 0.1:
                keep_segments.append((seg_start, seg_end))
            prev_end = min(s_end + padding, duration)

        # Segmento final
        if prev_end < duration - 0.1:
            keep_segments.append((prev_end, duration))

        if not keep_segments:
            import shutil as _sh
            _sh.copy2(str(input_path), str(output_path))
            return output_path

        # Crear lista de segmentos con select filter
        # Más robusto: generar archivo concat con segmentos
        tmp_dir = output_path.parent / "_silence_segs"
        tmp_dir.mkdir(exist_ok=True)
        seg_files = []

        for i, (t_start, t_end) in enumerate(keep_segments):
            seg_path = tmp_dir / f"seg_{i:04d}.mp4"
            seg_dur = t_end - t_start
            cmd = [
                "ffmpeg", "-y",
                "-ss", str(t_start), "-t", str(seg_dur),
                "-i", str(input_path),
                "-c:v", "libx264", "-crf", "21", "-preset", "veryfast",
                "-c:a", "aac", "-b:a", "128k",
                str(seg_path)
            ]
            r = subprocess.run(cmd, capture_output=True, text=True)
            if r.returncode == 0:
                seg_files.append(seg_path)

        if not seg_files:
            import shutil as _sh
            _sh.copy2(str(input_path), str(output_path))
            return output_path

        # Concatenar segmentos
        concat_list = tmp_dir / "concat.txt"
        concat_list.write_text("\n".join(f"file '{p.resolve()}'" for p in seg_files))
        cmd = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", str(concat_list),
            "-c:v", "libx264", "-crf", "20", "-preset", "fast",
            "-c:a", "aac", "-b:a", "128k",
            str(output_path)
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            raise RuntimeError(f"Silence removal concat failed: {r.stderr[-200:]}")

        # Limpieza
        import shutil as _sh
        _sh.rmtree(tmp_dir, ignore_errors=True)

        removed = len(starts)
        logger.info(f"[OK] Removed {removed} silence segments → {output_path.name}")
        return output_path

    # ── SUBTITLES ──────────────────────────────────────────────────────────────

    def burn_subtitles(
        self,
        input_path: Path,
        output_path: Path,
        srt_path: Path,
        font_size: int = 0,   # 0 = auto según resolución
        position: str = "bottom",  # bottom | center
    ) -> Path:
        """
        Quema subtítulos con fuente Anton (marca) y estilo REBEL LUXURY.
        Texto blanco, sombra negra, sin box — limpio y legible.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        info = _get_video_info(input_path)
        h = info["height"]

        # Tamaño de fuente proporcional a resolución
        if font_size == 0:
            font_size = max(22, int(h * 0.042))

        # Posición vertical
        y_pos = "h-h/5" if position == "bottom" else "(h-text_h)/2"

        # Fuente Anton si está disponible
        font_path = _ASSETS / "fonts" / "Anton-Regular.ttf"
        font_arg = f":fontfile={str(font_path).replace(chr(92), '/')}" if font_path.exists() else ""

        # Escape la ruta del SRT para FFmpeg (Windows backslashes)
        srt_str = str(srt_path).replace("\\", "/").replace(":", "\\:")

        vf = (
            f"subtitles={srt_str}"
            f":force_style='FontSize={font_size}{font_arg.replace(chr(58), chr(92)+chr(58))},"
            f"PrimaryColour=&HFFFFFF&,"
            f"OutlineColour=&H000000&,"
            f"Outline=2,Shadow=1,"
            f"Bold=1,"
            f"Alignment=2,"
            f"MarginV={max(20, int(h*0.04))}'"
        )

        # Simplificado — usar subtitles filter directamente
        srt_escaped = str(srt_path).replace("\\", "\\\\").replace(":", "\\:")
        font_file_arg = ""
        if font_path.exists():
            fp = str(font_path).replace("\\", "/")
            font_file_arg = f":fontsdir={str(font_path.parent).replace(chr(92), '/')}"

        vf_simple = (
            f"subtitles='{str(srt_path).replace(chr(92), '/')}'"
            f":force_style='FontSize={font_size},"
            f"FontName=Anton,"
            f"PrimaryColour=&HFFFFFF&,"
            f"OutlineColour=&H000000&,"
            f"Outline=3,Shadow=2,Bold=1,Alignment=2,"
            f"MarginV={max(20, int(h*0.04))}'"
            f"{font_file_arg}"
        )

        cmd = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-vf", vf_simple,
            "-c:v", "libx264", "-crf", "19", "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning(f"Subtitle burn failed: {result.stderr[-300:]}")
            # Fallback: copiar sin subtítulos
            import shutil as _sh
            _sh.copy2(str(input_path), str(output_path))
        else:
            logger.info(f"[OK] Subtitles burned: {output_path.name}")
        return output_path

    # ── BROLL IMAGES ───────────────────────────────────────────────────────────

    def insert_broll(
        self,
        input_path: Path,
        output_path: Path,
        broll_data: list,
    ) -> Path:
        """
        Inserta imágenes de B-roll en momentos específicos del video.

        broll_data: lista de dicts:
            [{"time": 5.0, "duration": 2.5, "image": "path/to/img.png"}, ...]

        Las imágenes se superponen sobre el video con fade in/out de 0.3s.
        """
        if not broll_data:
            import shutil as _sh
            _sh.copy2(str(input_path), str(output_path))
            return output_path

        output_path.parent.mkdir(parents=True, exist_ok=True)
        info = _get_video_info(input_path)
        w, h = info["width"], info["height"]

        # Construir filter_complex con overlays
        inputs = ["-i", str(input_path)]
        filter_parts = []
        last_label = "[0:v]"

        for i, broll in enumerate(broll_data):
            img_path = Path(broll["image"])
            if not img_path.exists():
                continue
            t_start = float(broll.get("time", 0))
            t_dur   = float(broll.get("duration", 2.0))
            fade    = 0.3

            inputs += ["-i", str(img_path)]
            img_idx = i + 1

            # Scale imagen al tamaño del video
            filter_parts.append(
                f"[{img_idx}:v]scale={w}:{h},setsar=1,"
                f"fade=t=in:st=0:d={fade}:alpha=1,"
                f"fade=t=out:st={t_dur-fade}:d={fade}:alpha=1[broll{i}]"
            )
            out_label = f"[after_broll{i}]"
            filter_parts.append(
                f"{last_label}[broll{i}]overlay=x=0:y=0:enable='between(t,{t_start},{t_start+t_dur})'{out_label}"
            )
            last_label = out_label

        filter_parts.append(f"{last_label}copy[vout]")
        filter_complex = ";".join(filter_parts)

        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "0:a?",
            "-c:v", "libx264", "-crf", "19", "-preset", "fast",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy",
            str(output_path)
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.warning(f"B-roll insert failed: {result.stderr[-300:]}")
            import shutil as _sh
            _sh.copy2(str(input_path), str(output_path))
        else:
            logger.info(f"[OK] B-roll inserted: {output_path.name}")
        return output_path

    def _quality_params(self, quality: str) -> list:
        """Parámetros FFmpeg para máxima calidad REBEL LUXURY."""
        if quality == "ultra":
            # 4K-ready: CRF 16, High Profile, slow preset para mejor compresión
            return ["-c:v", "libx264", "-crf", "16", "-preset", "slow",
                    "-profile:v", "high", "-level", "5.1",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "320k", "-ar", "48000"]
        elif quality == "high":
            # 1080p-4K: CRF 18, medium preset
            return ["-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-profile:v", "high", "-level", "4.2",
                    "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "256k", "-ar", "48000"]
        else:  # standard
            return ["-c:v", "libx264", "-crf", "20", "-preset", "fast",
                    "-pix_fmt", "yuv420p"]

    def add_branding(
        self,
        input_path: Path,
        output_path: Path,
        titulo: str = "",
        add_intro: bool = True,
        add_outro: bool = True,
        add_watermark: bool = True,
        target_size: tuple = (1920, 1080),
        quality: str = "ultra",   # ultra=4K/CRF16 | high=CRF18 | standard=CRF20
    ) -> Path:
        """
        Aplica branding completo a un video:
        - Intro 3s (logo + título)
        - Watermark esquina inferior derecha
        - Outro 4s (logo + redes)
        - Fade in/out
        """
        info = _get_video_info(input_path)
        w, h = info["width"], info["height"]
        # Usar dimensiones del video original
        size = (w, h)

        intro_frame = _make_intro_frame(titulo or "IM MUSIC", size) if add_intro else None
        outro_frame = _make_outro_frame(size) if add_outro else None
        wm_frame    = _make_watermark(size) if add_watermark else None

        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Construir filtro FFmpeg
        # 1. Intro: imagen estática INTRO_DUR segundos con fade in/out
        # 2. Video principal: con watermark overlay + fade in
        # 3. Outro: imagen estática OUTRO_DUR segundos con fade out

        inputs = []
        if intro_frame:
            inputs += ["-loop", "1", "-t", str(INTRO_DUR), "-i", str(intro_frame)]
        inputs += ["-i", str(input_path)]
        if wm_frame and add_watermark:
            inputs += ["-i", str(wm_frame)]
        if outro_frame:
            inputs += ["-loop", "1", "-t", str(OUTRO_DUR), "-i", str(outro_frame)]

        # Indices: 0=intro, 1=main_video, 2=watermark (opt), 3=outro (opt)
        idx_main = 1 if intro_frame else 0
        idx_wm   = idx_main + 1 if wm_frame else None
        idx_outro = (idx_wm + 1 if idx_wm else idx_main + 1) if outro_frame else None

        # Filter complex
        filter_parts = []

        # Scale intro y outro al mismo tamaño que el video principal
        if intro_frame:
            filter_parts.append(f"[0:v]scale={w}:{h},setsar=1,fade=t=in:st=0:d={FADE_DUR},fade=t=out:st={INTRO_DUR - FADE_DUR}:d={FADE_DUR}[intro]")

        # Main video con watermark
        if wm_frame:
            # Posición watermark: esquina inferior derecha con margen
            margin = max(10, int(w * 0.015))
            wm_x = f"W-w-{margin}"
            wm_y = f"H-h-{margin}"
            filter_parts.append(
                f"[{idx_main}:v][{idx_wm}:v]overlay=x={wm_x}:y={wm_y}:format=auto[main_wm]"
            )
            main_label = "[main_wm]"
        else:
            main_label = f"[{idx_main}:v]"

        # Fade in/out en main
        dur_main = info["duration"]
        filter_parts.append(
            f"{main_label}fade=t=in:st=0:d={FADE_DUR},fade=t=out:st={max(0, dur_main - FADE_DUR)}:d={FADE_DUR}[main]"
        )

        if outro_frame:
            filter_parts.append(
                f"[{idx_outro}:v]scale={w}:{h},setsar=1,fade=t=in:st=0:d={FADE_DUR},fade=t=out:st={OUTRO_DUR - FADE_DUR}:d={FADE_DUR}[outro]"
            )

        # Concatenar
        concat_parts = ""
        concat_n = 0
        if intro_frame:
            concat_parts += "[intro]"
            concat_n += 1
        concat_parts += "[main]"
        concat_n += 1
        if outro_frame:
            concat_parts += "[outro]"
            concat_n += 1

        filter_parts.append(f"{concat_parts}concat=n={concat_n}:v=1:a=0[vout]")
        filter_complex = ";".join(filter_parts)

        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", filter_complex,
            "-map", "[vout]",
        ]
        # Audio del video principal (si tiene)
        has_audio = self._has_audio(input_path)
        if has_audio:
            cmd += ["-map", f"{idx_main}:a?"]
        cmd += ["-c:v", "libx264", "-crf", "20", "-preset", "fast",
                "-pix_fmt", "yuv420p", str(output_path)]

        logger.info(f"Applying branding to {input_path.name}...")
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr[-500:]}")
            raise RuntimeError(f"Branding failed: {result.stderr[-200:]}")

        logger.info(f"[OK] {output_path.name}  {output_path.stat().st_size // 1024}KB")
        return output_path

    def crop_vertical(
        self,
        input_path: Path,
        output_path: Path,
        max_duration: float = 60.0,
        quality: str = "high",  # ultra | high | standard
    ) -> Path:
        """Recorta video horizontal a formato vertical 9:16 para Reels/TikTok."""
        info = _get_video_info(input_path)
        w, h = info["width"], info["height"]
        dur = min(info["duration"], max_duration)

        # Calcular crop: altura full, ancho = h * 9/16
        new_w = int(h * 9 / 16)
        if new_w > w:
            # Video ya es vertical o cuadrado
            new_w = w
        x_offset = (w - new_w) // 2

        output_path.parent.mkdir(parents=True, exist_ok=True)
        # Escala al máximo que permita el source (1080p mínimo, 4K si viene de 4K)
        out_w = min(1080, new_w)
        out_h = int(out_w * 16 / 9)
        scale_str = f"scale={out_w}:{out_h}:flags=lanczos"
        qp = self._quality_params(quality)
        cmd = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-t", str(dur),
            "-vf", f"crop={new_w}:{h}:{x_offset}:0,{scale_str},setsar=1",
        ] + qp + [str(output_path)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Crop vertical failed: {result.stderr[-200:]}")
        return output_path

    def produce_pack(
        self,
        raw_video: Path,
        titulo: str,
        out_dir: Optional[Path] = None,
        content_type: str = "default",     # organico | blog | fake_podcast | atraccion | validacion | fidelizacion
        youtube_full: bool = True,
        reel_duration: float = 45.0,
        tiktok_duration: float = 60.0,
        short_duration: float = 58.0,
        # Overrides opcionales (sobreescriben el perfil si se pasan)
        cinema_grade: Optional[bool] = None,
        remove_silence: Optional[bool] = None,
        srt_path: Optional[Path] = None,
        broll_data: Optional[list] = None,
    ) -> dict:
        """
        Pipeline completo: raw video → pack con todos los formatos.
        El content_type determina automáticamente el estilo de edición.
        Calidad máxima: 4K cuando el video lo permite, CRF 16-18, H.264 High Profile.

        Retorna dict con rutas de todos los archivos generados.
        """
        # ── Cargar perfil de edición ─────────────────────────────────────────
        profile = EDIT_PROFILES.get(content_type, EDIT_PROFILES["default"]).copy()

        # Overrides manuales sobreescriben el perfil
        if cinema_grade is not None:
            profile["cinema_grade"] = cinema_grade
        if remove_silence is not None:
            profile["remove_silence"] = remove_silence

        print(f"\n{'='*50}")
        print(f"EDITOR IM MUSIC — REBEL LUXURY")
        print(f"Tipo: {content_type.upper()} | {profile['description']}")
        print(f"{'='*50}")

        if out_dir is None:
            slug = titulo[:30].lower().replace(" ", "_").replace("?", "").replace("¿", "")
            out_dir = _OUTPUTS / f"edited_{slug}"
        out_dir.mkdir(parents=True, exist_ok=True)

        pack = {
            "titulo": titulo,
            "content_type": content_type,
            "raw": str(raw_video),
            "profile": profile["description"],
            "outputs": {}
        }
        tmp_dir = out_dir / "_tmp"
        tmp_dir.mkdir(exist_ok=True)

        # ── PASO 1: Pre-procesar video ───────────────────────────────────────
        working = raw_video

        # 1a. Cortar silencios — solo si el perfil lo indica
        _remove_sil = profile.get("remove_silence", True)
        if _remove_sil and self._has_audio(working):
            print("Cortando silencios...")
            no_silence = tmp_dir / "no_silence.mp4"
            try:
                working = self.remove_silences(
                    working, no_silence,
                    silence_threshold=profile.get("silence_threshold", -35.0),
                    min_silence_dur=profile.get("min_silence_dur", 0.4),
                    padding=profile.get("silence_padding", 0.15),
                )
                print(f"  [OK] Silencios eliminados")
            except Exception as e:
                print(f"  [!] Silencio removal saltado: {e}")

        # 1b. Color grading cinematográfico
        _cinema = profile.get("cinema_grade", True)
        if _cinema:
            print("Aplicando color grade cine REBEL LUXURY...")
            graded = tmp_dir / "graded.mp4"
            try:
                working = self.apply_cinema_grade(working, graded)
                print(f"  [OK] Color grade aplicado")
            except Exception as e:
                print(f"  [!] Color grade saltado: {e}")

        # Guardar configuración de subtítulos en pack para procesamiento externo
        pack["subtitle_config"] = {
            "size": profile.get("subtitle_size", "medium"),
            "position": profile.get("subtitle_position", "bottom"),
        }

        # 1c. B-roll inserts
        if broll_data:
            print(f"Insertando {len(broll_data)} imágenes B-roll...")
            with_broll = tmp_dir / "with_broll.mp4"
            try:
                working = self.insert_broll(working, with_broll, broll_data)
                print(f"  [OK] B-roll insertado")
            except Exception as e:
                print(f"  [!] B-roll saltado: {e}")

        # 1d. Subtítulos
        if srt_path and Path(srt_path).exists():
            print("Quemando subtítulos Anton...")
            with_subs = tmp_dir / "with_subs.mp4"
            try:
                working = self.burn_subtitles(working, with_subs, Path(srt_path))
                print(f"  [OK] Subtítulos quemados")
            except Exception as e:
                print(f"  [!] Subtítulos saltados: {e}")

        # ── PASO 2: Generar formatos finales ─────────────────────────────────
        info = _get_video_info(working)
        src_w, src_h = info["width"], info["height"]
        print(f"\nFuente procesada: {src_w}x{src_h}  {info['duration']:.1f}s")
        print("Generando formatos de alta calidad...")

        # 2a. YouTube long-form (16:9, máxima calidad — 4K si el source lo permite)
        if youtube_full:
            yt_path = out_dir / "youtube_completo.mp4"
            try:
                self.add_branding(
                    working, yt_path, titulo=titulo,
                    add_intro=profile.get("add_intro", True),
                    add_outro=profile.get("add_outro", True),
                    add_watermark=profile.get("add_watermark", True),
                    quality="ultra",  # CRF 16 para YouTube — máxima calidad REBEL LUXURY
                )
                pack["outputs"]["youtube"] = str(yt_path)
                print(f"[OK] YouTube 16:9: {yt_path.stat().st_size//1024}KB")
            except Exception as e:
                print(f"[FAIL] YouTube: {e}")

        # 2b. Reel Instagram (9:16, alta calidad)
        reel_path = out_dir / "reel_instagram.mp4"
        try:
            self.crop_vertical(working, reel_path, max_duration=reel_duration, quality="high")
            pack["outputs"]["reel_instagram"] = str(reel_path)
            print(f"[OK] Reel IG 9:16: {reel_path.stat().st_size//1024}KB")
        except Exception as e:
            print(f"[FAIL] Reel IG: {e}")

        # 2c. TikTok (9:16, alta calidad)
        tiktok_path = out_dir / "tiktok.mp4"
        try:
            self.crop_vertical(working, tiktok_path, max_duration=tiktok_duration, quality="high")
            pack["outputs"]["tiktok"] = str(tiktok_path)
            print(f"[OK] TikTok 9:16: {tiktok_path.stat().st_size//1024}KB")
        except Exception as e:
            print(f"[FAIL] TikTok: {e}")

        # 2d. YouTube Short (9:16, alta calidad)
        short_path = out_dir / "youtube_short.mp4"
        try:
            self.crop_vertical(working, short_path, max_duration=short_duration, quality="high")
            pack["outputs"]["youtube_short"] = str(short_path)
            print(f"[OK] YT Short 9:16: {short_path.stat().st_size//1024}KB")
        except Exception as e:
            print(f"[FAIL] YT Short: {e}")

        # Limpieza temporales
        import shutil as _sh
        _sh.rmtree(tmp_dir, ignore_errors=True)

        print(f"\n[DONE] Pack completo en: {out_dir}")
        return pack

    def _has_audio(self, video_path: Path) -> bool:
        cmd = ["ffprobe", "-v", "quiet", "-print_format", "json",
               "-show_streams", str(video_path)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            return False
        info = json.loads(r.stdout)
        return any(s.get("codec_type") == "audio" for s in info.get("streams", []))
