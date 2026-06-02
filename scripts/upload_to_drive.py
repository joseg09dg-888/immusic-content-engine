"""
Upload content pieces to Google Drive using service account or OAuth token.
Organizes files under: IM Music - Content Engine/CONTENIDO/YYYY/MM_Mes/DATE_Titulo/

Run:
    python scripts/upload_to_drive.py --folder outputs/carousel_v2 --date 2026-06-01 --titulo "JAQUEAMOS MENTES"
"""
import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from dotenv import load_dotenv
load_dotenv()

# Drive folder IDs (created 2026-06-01)
DRIVE_ROOT        = "1dQLflEFXZMU0C9viIZjvmu7bWKnmUZG3"
DRIVE_CONTENIDO   = "1btnNec-WJlTJ6DsDf-bir185tPcIJXy5"
DRIVE_2026        = "1EIEjGHFUrmTVqCL2ou-1yHij1vF5i-jh"
DRIVE_JUNIO       = "11BWeOUKpmAzUPHBmAYO8RhMYQ1XCBqmS"
DRIVE_CARRUSELES  = "1vjBlbr4l2_bypEhjK2pR1PSbIHQI9kSA"
DRIVE_REELS       = "1VACe3VQRCLI0lFAhckNxdwhcpooLa0Zq"
DRIVE_THUMBNAILS  = "1SZIOoW0UKZj7PkLzPLnHFtWAFW13bCrq"
DRIVE_STORIES     = "10NB71wp_bud9VDOug5p1zq03aEReM2-E"
DRIVE_APROBADOS   = "1rQN7ELvrGb3KhLMXQIW6-eeaQGy9yUtA"
DRIVE_PUBLICADOS  = "1ZmHi3jhci3xIua60e7VLHt8UhMwbjU63"

MONTHS = {
    "01": "01_Enero", "02": "02_Febrero", "03": "03_Marzo",
    "04": "04_Abril", "05": "05_Mayo",    "06": "06_Junio",
    "07": "07_Julio", "08": "08_Agosto",  "09": "09_Septiembre",
    "10": "10_Octubre","11": "11_Noviembre","12": "12_Diciembre",
}

DAYS_ES = {0: "Lunes", 1: "Martes", 2: "Miercoles",
           3: "Jueves", 4: "Viernes", 5: "Sabado", 6: "Domingo"}


def build_drive_service():
    """Build Google Drive service using stored OAuth token or service account."""
    token_file = Path(__file__).resolve().parent.parent / ".youtube_token.json"
    if token_file.exists():
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        creds = Credentials.from_authorized_user_file(str(token_file))
        return build("drive", "v3", credentials=creds)
    raise RuntimeError("No credentials found. Run OAuth setup first.")


def get_or_create_folder(service, name: str, parent_id: str) -> str:
    """Get existing folder or create it."""
    q = (f"mimeType='application/vnd.google-apps.folder' "
         f"and name='{name}' and '{parent_id}' in parents and trashed=false")
    res = service.files().list(q=q, fields="files(id,name)").execute()
    files = res.get("files", [])
    if files:
        return files[0]["id"]
    meta = {"name": name, "mimeType": "application/vnd.google-apps.folder",
            "parents": [parent_id]}
    f = service.files().create(body=meta, fields="id").execute()
    return f["id"]


def upload_file(service, file_path: Path, parent_id: str) -> str:
    """Upload a file to Drive folder. Returns file ID."""
    from googleapiclient.http import MediaFileUpload
    import mimetypes
    mime = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
    meta = {"name": file_path.name, "parents": [parent_id]}
    media = MediaFileUpload(str(file_path), mimetype=mime)
    f = service.files().create(body=meta, media_body=media, fields="id,webViewLink").execute()
    return f["id"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--folder", required=True, help="Local folder with output files")
    parser.add_argument("--date", required=True, help="Publication date YYYY-MM-DD")
    parser.add_argument("--titulo", required=True, help="Content title for folder name")
    parser.add_argument("--tipo", default="carousel", choices=["carousel","reel","story","thumbnail"])
    args = parser.parse_args()

    folder = Path(args.folder)
    if not folder.exists():
        print(f"[ERROR] Folder not found: {folder}")
        sys.exit(1)

    dt = datetime.strptime(args.date, "%Y-%m-%d")
    year = str(dt.year)
    month_key = f"{dt.month:02d}"
    month_folder = MONTHS.get(month_key, f"{month_key}_Mes")
    day_name = DAYS_ES[dt.weekday()]
    day_folder = f"{args.date} {day_name} - {args.titulo}"

    print(f"Uploading to Drive: {year}/{month_folder}/{day_folder}/")

    try:
        service = build_drive_service()
    except Exception as e:
        print(f"[ERROR] Drive auth failed: {e}")
        print("  Make sure .youtube_token.json has Drive scope or re-run OAuth.")
        sys.exit(1)

    # Get/create year/month/day folders
    year_id  = get_or_create_folder(service, year, DRIVE_CONTENIDO)
    month_id = get_or_create_folder(service, month_folder, year_id)
    day_id   = get_or_create_folder(service, day_folder, month_id)

    # Also upload to type-specific folder
    type_folders = {
        "carousel":  DRIVE_CARRUSELES,
        "reel":      DRIVE_REELS,
        "story":     DRIVE_STORIES,
        "thumbnail": DRIVE_THUMBNAILS,
    }
    type_parent = type_folders.get(args.tipo, DRIVE_CARRUSELES)
    type_day_id = get_or_create_folder(service, day_folder, type_parent)

    files = sorted(folder.glob("*.*"))
    if not files:
        print("[!] No files found in folder")
        sys.exit(1)

    uploaded = 0
    for f in files:
        try:
            fid = upload_file(service, f, day_id)
            upload_file(service, f, type_day_id)
            print(f"  [OK] {f.name}  (id={fid})")
            uploaded += 1
        except Exception as e:
            print(f"  [FAIL] {f.name}: {e}")

    print(f"\nDone. {uploaded}/{len(files)} files uploaded.")
    print(f"View at: https://drive.google.com/drive/folders/{day_id}")


if __name__ == "__main__":
    main()
