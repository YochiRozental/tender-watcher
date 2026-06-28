import time

import requests

from src.config import MAKE_WEBHOOK_URL


def send_single_item(item: dict) -> bool:
    if not MAKE_WEBHOOK_URL:
        print("MAKE_WEBHOOK_URL is missing. Skipping Make notification.")
        return False

    for attempt in range(1, 4):
        try:
            response = requests.post(
                MAKE_WEBHOOK_URL,
                json=item,
                timeout=30,
            )
            response.raise_for_status()
            return True

        except requests.RequestException as error:
            print(f"Failed to send item to Make. Attempt {attempt}/3")
            print(f"Title: {item.get('title')}")
            print(f"URL: {item.get('url')}")
            print(f"Error: {error}")

            if attempt < 3:
                time.sleep(5)

    return False


def send_to_make(items: list[dict]) -> None:
    if not items:
        print("No items to send to Make.")
        return

    sent_count = 0
    failed_count = 0

    for item in items:
        if send_single_item(item):
            sent_count += 1
        else:
            failed_count += 1

    print(f"Make notification summary: sent={sent_count}, failed={failed_count}")
