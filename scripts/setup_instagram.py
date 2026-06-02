"""Run once to authenticate Instagram and save session to .instagram_session.json"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv()

from instagrapi import Client

SESSION_FILE = Path(__file__).resolve().parent.parent / ".instagram_session.json"

username = os.environ["INSTAGRAM_USERNAME"]
password = os.environ["INSTAGRAM_PASSWORD"]

cl = Client()
cl.login(username, password)
cl.dump_settings(SESSION_FILE)
print(f"[OK] Instagram session saved -> {SESSION_FILE}")
print(f"     User: @{username}  |  pk: {cl.user_id}")
