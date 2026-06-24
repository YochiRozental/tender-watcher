import json

from src.config import SEEN_URLS_FILE


def load_seen_urls() -> set[str]:
    if not SEEN_URLS_FILE.exists():
        return set()

    with open(SEEN_URLS_FILE, "r", encoding="utf-8") as file:
        return set(json.load(file))


def save_seen_urls(urls: set[str]) -> None:
    SEEN_URLS_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(SEEN_URLS_FILE, "w", encoding="utf-8") as file:
        json.dump(sorted(urls), file, ensure_ascii=False, indent=2)
