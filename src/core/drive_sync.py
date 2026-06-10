"""
Google Drive Auto-Sync para IM Music Content Engine.
Detecta la carpeta de Drive for Desktop y guarda contenido ahí directo.
Cuando Drive está instalado, el contenido aparece en Drive sin hacer nada más.
"""
import shutil
from datetime import datetime
from pathlib import Path

# Carpeta IM Music en Drive (se crea automáticamente si no existe)
DRIVE_FOLDER_NAME = "IM Music - Content Engine"
DRIVE_PRUEBAS_NAME = "PRUEBAS - Contenido en Desarrollo"
DRIVE_POR_FECHA_NAME = "📅 CONTENIDO - Por Fecha"

MESES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
         "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]


def _find_drive_root() -> Path | None:
    """Encuentra la carpeta raíz de Google Drive for Desktop."""
    user = Path.home()

    # Google Drive for Desktop monta como unidad virtual.
    # El nombre de la carpeta depende del idioma de la cuenta:
    # "My Drive" (EN) o "Mi unidad" (ES).
    for drive_letter in ['G', 'H', 'I', 'J', 'K', 'L']:
        for name in ("My Drive", "Mi unidad"):
            p = Path(f"{drive_letter}:/{name}")
            if p.exists():
                return p

    # Google Drive para Escritorio (versión nueva) en carpeta del usuario
    candidates = [
        user / "Google Drive" / "My Drive",
        user / "Google Drive" / "Mi unidad",
        user / "Google Drive",
        user / "My Drive",
        user / "Mi unidad",
    ]
    for p in candidates:
        if p.exists():
            return p

    return None


def get_output_dir(content_date: str, content_title: str = "pack") -> Path:
    """
    Retorna la carpeta donde guardar el contenido.
    Si Drive está disponible → guarda en Drive (sincroniza automáticamente).
    Si no → guarda local en outputs/.
    """
    drive_root = _find_drive_root()

    if drive_root:
        # Crear estructura en Drive
        im_folder = drive_root / DRIVE_FOLDER_NAME
        pruebas   = im_folder / DRIVE_PRUEBAS_NAME
        day_folder = pruebas / f"{content_date}_{content_title[:30]}"
        day_folder.mkdir(parents=True, exist_ok=True)
        print(f"[Drive] Guardando en: {day_folder}")
        return day_folder
    else:
        # Fallback local
        local = Path(__file__).resolve().parent.parent.parent / "outputs" / f"{content_date}_{content_title[:30]}"
        local.mkdir(parents=True, exist_ok=True)
        print(f"[Local] Drive no encontrado. Guardando en: {local}")
        return local


def sync_folder_to_drive(local_dir: Path, subfolder: str = "PRUEBAS") -> bool:
    """
    Copia una carpeta local a Drive for Desktop.
    Returns True si se copió a Drive, False si Drive no está disponible.
    """
    drive_root = _find_drive_root()
    if not drive_root:
        print("[!] Google Drive for Desktop no encontrado.")
        print("    Instala desde: google.com/drive/download")
        print(f"    Tu contenido está en: {local_dir}")
        return False

    dest = drive_root / DRIVE_FOLDER_NAME / subfolder / local_dir.name
    if dest.exists():
        print(f"[Drive] Ya existe: {dest.name}")
        return True

    print(f"[Drive] Copiando {local_dir.name} a Drive...")
    shutil.copytree(str(local_dir), str(dest))
    size_mb = sum(f.stat().st_size for f in dest.rglob('*') if f.is_file()) / (1024*1024)
    print(f"[OK] {dest.name} → Drive ({size_mb:.1f}MB)")
    return True


def sync_pack_to_drive(work_dir: Path, titulo: str, fecha: datetime = None) -> Path | None:
    """
    Copia el pack diario del autopilot (work_dir) a la carpeta de Drive
    'CONTENIDO - Por Fecha/{año}/{mes}_{Mes}/{fecha} {dia} - {titulo} (PENDIENTE APROBACION)'.
    Returns la ruta destino en Drive, o None si Drive no está disponible.
    """
    drive_root = _find_drive_root()
    if not drive_root:
        print("[!] Google Drive for Desktop no encontrado — pack se queda solo local.")
        return None

    fecha = fecha or datetime.now()
    mes_folder = f"{fecha.month:02d}_{MESES[fecha.month - 1]}"
    dia_nombre = DIAS[fecha.weekday()]
    safe_titulo = "".join(c for c in titulo if c not in '<>:"/\\|?*').strip()
    dest_name = f"{fecha:%Y-%m-%d} {dia_nombre} - {safe_titulo} (PENDIENTE APROBACION)"

    dest = (drive_root / DRIVE_FOLDER_NAME / DRIVE_POR_FECHA_NAME
            / str(fecha.year) / mes_folder / dest_name)
    dest.mkdir(parents=True, exist_ok=True)

    print(f"[Drive] Copiando pack a: {dest}")
    shutil.copytree(str(work_dir), str(dest), dirs_exist_ok=True)
    size_mb = sum(f.stat().st_size for f in dest.rglob('*') if f.is_file()) / (1024 * 1024)
    print(f"[OK] Pack en Drive ({size_mb:.1f}MB): {dest}")
    return dest


def is_drive_available() -> bool:
    return _find_drive_root() is not None


def drive_status() -> str:
    root = _find_drive_root()
    if root:
        return f"Drive disponible: {root}"
    return "Drive NO disponible — instala desde google.com/drive/download"
