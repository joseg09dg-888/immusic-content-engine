"""
Upload human-recorded content to Drive automatically.

Workflow:
  1. Graba tu video en telefono/camara
  2. Copia el archivo a la carpeta local que prefieras
  3. Ejecuta este script con la ruta del archivo
  4. El script lo sube a la carpeta correcta en Drive
  5. Si es RAW → va a "Videos Raw - Sin Editar"
  6. Si es EDITADO → va a "Videos Editados - Listos"

Uso:
    python scripts/upload_human_content.py --file "mi_video.mp4" --tipo raw --titulo "Por que fracasan los artistas"
    python scripts/upload_human_content.py --file "mi_video_editado.mp4" --tipo editado --titulo "Por que fracasan los artistas"
    python scripts/upload_human_content.py --file "guion.txt" --tipo guion --titulo "Guion lunes 2026-06-03"
"""
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

# IDs de carpetas Drive (CONTENIDO HUMANO)
DRIVE_HUMANO_ROOT   = "1neBsyLvYLJ5gKxL8O_OUux86u0JTecyH"
DRIVE_GUIONES       = "1kfJsWqOOIqbz-gYQLAIdV3DUO6sHdNHX"
DRIVE_VIDEOS_RAW    = "12mgf_IzzkeUnKdILBmrll9UO4wE84-HZ"
DRIVE_VIDEOS_LISTOS = "1KNXojw2d7hCYJAOOX91stJTPR68RjkM3"

# Carpetas del contenido automatico (para cross-reference)
DRIVE_APROBADOS     = "1rQN7ELvrGb3KhLMXQIW6-eeaQGy9yUtA"
DRIVE_PUBLICADOS    = "1ZmHi3jhci3xIua60e7VLHt8UhMwbjU63"

FOLDER_MAP = {
    "guion":   DRIVE_GUIONES,
    "raw":     DRIVE_VIDEOS_RAW,
    "editado": DRIVE_VIDEOS_LISTOS,
}


def build_drive_service():
    token_file = Path(__file__).resolve().parent.parent / ".youtube_token.json"
    if not token_file.exists():
        raise RuntimeError("No hay token OAuth. El token de YouTube puede no tener scope de Drive.")
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build
    creds = Credentials.from_authorized_user_file(str(token_file))
    return build("drive", "v3", credentials=creds)


def upload_file(service, file_path: Path, parent_id: str, title: str = None) -> dict:
    from googleapiclient.http import MediaFileUpload
    import mimetypes
    mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    name = title or file_path.name
    meta = {"name": name, "parents": [parent_id]}
    media = MediaFileUpload(str(file_path), mimetype=mime, resumable=True)
    result = service.files().create(
        body=meta, media_body=media, fields="id,name,webViewLink,size"
    ).execute()
    return result


def main():
    parser = argparse.ArgumentParser(description="Sube contenido humano a Drive")
    parser.add_argument("--file", required=True, help="Ruta del archivo a subir")
    parser.add_argument("--tipo", required=True,
                        choices=["guion", "raw", "editado"],
                        help="Tipo: guion | raw (sin editar) | editado (listo)")
    parser.add_argument("--titulo", required=True, help="Titulo del contenido")
    parser.add_argument("--fecha", default=datetime.now().strftime("%Y-%m-%d"),
                        help="Fecha YYYY-MM-DD (default: hoy)")
    args = parser.parse_args()

    file_path = Path(args.file)
    if not file_path.exists():
        print(f"[ERROR] Archivo no encontrado: {file_path}")
        sys.exit(1)

    size_mb = file_path.stat().st_size / (1024 * 1024)
    print(f"Archivo: {file_path.name}  ({size_mb:.1f} MB)")
    print(f"Tipo: {args.tipo}  |  Titulo: {args.titulo}")

    parent_id = FOLDER_MAP[args.tipo]
    drive_name = {
        "guion":   "Guiones - Para Grabar",
        "raw":     "Videos Raw - Sin Editar",
        "editado": "Videos Editados - Listos",
    }[args.tipo]
    print(f"Destino Drive: {drive_name}")

    # Nombre final en Drive incluye fecha + titulo
    ext = file_path.suffix
    drive_filename = f"{args.fecha} - {args.titulo}{ext}"

    try:
        service = build_drive_service()
        print(f"Subiendo... (puede tardar para videos grandes)")
        result = upload_file(service, file_path, parent_id, drive_filename)
        size_kb = int(result.get("size", 0)) // 1024
        print(f"[OK] Subido: {result['name']}")
        print(f"     ID: {result['id']}")
        print(f"     Link: {result.get('webViewLink', 'N/A')}")
        print(f"     Tamaño: {size_kb} KB")
        print()
        if args.tipo == "editado":
            print("Video listo para publicar.")
            print(f"Muevelo a APROBADOS cuando quieras publicarlo:")
            print(f"  Drive > APROBADOS: https://drive.google.com/drive/folders/{DRIVE_APROBADOS}")
    except Exception as e:
        print(f"[ERROR] Upload fallido: {e}")
        print()
        print("Si el token no tiene scope de Drive, ejecuta:")
        print("  python scripts/setup_youtube_auth.py --scopes drive")
        sys.exit(1)


if __name__ == "__main__":
    main()
