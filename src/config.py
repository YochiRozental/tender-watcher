from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

SOURCES_FILE = DATA_DIR / "sources.json"
CANDIDATE_SOURCES_FILE = DATA_DIR / "candidate_sources.json"

load_dotenv(BASE_DIR / ".env")

MAKE_WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")