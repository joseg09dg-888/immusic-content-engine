"""
Sincroniza TODOS los outputs a Google Drive automáticamente.
Sube imágenes PNG/JPG y videos MP4 a la carpeta correcta según la fecha.

Requiere: pip install google-auth google-auth-oauthlib google-api-python-client

Para autorizar Drive la primera vez:
  python scripts/setup_drive_auth.py

Uso:
  python scripts/sync_to_drive.py                    # sube outputs pendientes
  python scripts/sync_to_drive.py --folder outputs/LUNES_2026-06-03_PACK_COMPLETO
"""
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

# IDs Drive (ya creados)
DRIVE_PRUEBAS = "1rmIdD3WPxlEdYx4Ha2EYgSR0BIvyoO8k"
DRIVE_CARRUSELES = "1vjBlbr4l2_bypEhjK2pR1PSbIHQI9kSA"

_DRIVE_TOKEN   = Path(__file__).resolve().parent.parent / ".drive_token.json"
_YOUTUBE_TOKEN = Path(__file__).resolve().parent.parent / ".youtube_token.json"

DRIVE_SCOPES = [
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/youtube.upload",
]


def build_drive_service():
    """Construye el cliente Drive con OAuth. Abre browser si necesita autorización."""
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from google.auth.transport.requests import Request

    creds = None
    token_path = _DRIVE_TOKEN

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), DRIVE_SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Necesita credenciales OAuth de Google Cloud Console
            # Descarga oauth_credentials.json desde console.cloud.google.com
            creds_file = Path(__file__).resolve().parent.parent / "oauth_credentials.json"
            if not creds_file.exists():
                print("[ERROR] Falta oauth_credentials.json")
                print("Descárgalo de: console.cloud.google.com")
                print("APIs & Services > Credentials > OAuth 2.0 Client IDs > Download JSON")
                print(f"Guárdalo en: {creds_file}")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), DRIVE_SCOPES)
            creds = flow.run_local_server(port=8080, open_browser=True)

        token_path.write_text(creds.to_json())

    return build("drive", "v3", credentials=creds)


def upload_file(service, file_path: Path, parent_id: str, drive_name: str = None) -> str:
    """Sube un archivo a Drive. Retorna el ID del archivo."""
    from googleapiclient.http import MediaFileUpload
    import mimetypes

    mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    name = drive_name or file_path.name
    meta = {"name": name, "parents": [parent_id]}
    media = MediaFileUpload(str(file_path), mimetype=mime, resumable=True)
    result = service.files().create(
        body=meta, media_body=media, fields="id,name,size,webViewLink"
    ).execute()
    return result["id"]


def get_or_create_folder(service, name: str, parent_id: str) -> str:
    """Obtiene o crea una carpeta en Drive."""
    q = (f"name='{name}' and mimeType='application/vnd.google-apps.folder' "
         f"and '{parent_id}' in parents and trashed=false")
    res = service.files().list(q=q, fields="files(id)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]}
    f = service.files().create(body=meta, fields="id").execute()
    return f["id"]


def sync_folder(service, local_dir: Path, drive_parent_id: str, prefix: str = "") -> int:
    """Sube recursivamente todos los archivos de local_dir a Drive."""
    uploaded = 0
    for item in sorted(local_dir.iterdir()):
        if item.name.startswith("_") or item.name.startswith("."):
            continue
        if item.is_dir():
            sub_folder_id = get_or_create_folder(service, item.name, drive_parent_id)
            uploaded += sync_folder(service, item, sub_folder_id, prefix + "  ")
        elif item.suffix.lower() in (".png", ".jpg", ".jpeg", ".mp4", ".txt", ".md"):
            size_mb = item.stat().st_size / (1024 * 1024)
            print(f"{prefix}Subiendo {item.name} ({size_mb:.1f} MB)...", end=" ", flush=True)
            try:
                fid = upload_file(service, item, drive_parent_id)
                print(f"[OK] id={fid[:12]}")
                uploaded += 1
            except Exception as e:
                print(f"[FAIL] {e}")
    return uploaded


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", help="Carpeta local a subir (default: outputs/)")
    parser.add_argument("--date", help="Fecha YYYY-MM-DD para organizar en Drive")
    args = parser.parse_args()

    local_dir = Path(args.folder) if args.folder else Path("outputs")
    if not local_dir.exists():
        print(f"[ERROR] Carpeta no encontrada: {local_dir}")
        sys.exit(1)

    print(f"\nConectando con Google Drive...")
    service = build_drive_service()
    print("[OK] Conectado\n")

    # Crear carpeta en Drive PRUEBAS con nombre de fecha
    folder_name = local_dir.name
    if args.date:
        folder_name = f"{args.date} — {local_dir.name}"

    drive_folder_id = get_or_create_folder(service, folder_name, DRIVE_PRUEBAS)
    print(f"Carpeta Drive: {folder_name}")
    print(f"ID: {drive_folder_id}")
    print(f"Link: https://drive.google.com/drive/folders/{drive_folder_id}")
    print()

    uploaded = sync_folder(service, local_dir, drive_folder_id)
    print(f"\n[DONE] {uploaded} archivos subidos a Drive")


if __name__ == "__main__":
    main()
