import requests

from src.config import MAKE_WEBHOOK_URL


def send_to_make(items: list[dict]) -> None:
    if not items or not MAKE_WEBHOOK_URL:
        return

    for item in items:
        response = requests.post(
            MAKE_WEBHOOK_URL,
            json=item,
            timeout=30,
        )
        response.raise_for_status()