import json
from pathlib import Path


SEEN_FILE = Path("seen_urls.json")


def load_seen_urls() -> set[str]:
    if not SEEN_FILE.exists():
        return set()

    with open(SEEN_FILE, "r", encoding="utf-8") as file:
        return set(json.load(file))


def save_seen_urls(urls: set[str]) -> None:
    with open(SEEN_FILE, "w", encoding="utf-8") as file:
        json.dump(sorted(urls), file, ensure_ascii=False, indent=2)