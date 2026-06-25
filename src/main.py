import json
from datetime import date

from src.config import SOURCES_FILE
from src.notifier import send_to_make
from src.scraper import scan_source
from src.url_checker import is_url_accessible
from src.utils import encode_url


def load_sources() -> list[dict]:
    with open(SOURCES_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def collect_tenders(sources: list[dict]) -> list[dict]:
    all_results = []

    for source in sources:
        try:
            results = scan_source(source)
            print(f"{source['name']}: נמצאו {len(results)} תוצאות")
            all_results.extend(results)

        except Exception as error:
            print(f"שגיאה במקור {source['name']}: {error}")

    return all_results


def get_architecture_tenders(items: list[dict]) -> list[dict]:
    results = []
    seen_urls = set()

    for item in items:
        if not item["architecture_related"]:
            continue

        url = item["url"]

        if url in seen_urls:
            continue

        seen_urls.add(url)
        results.append(item)

    return results


def add_date_found(items: list[dict]) -> list[dict]:
    today = date.today().isoformat()

    return [
        {
            "date_found": today,
            **item,
            "safe_url": encode_url(item["url"]),
        }
        for item in items
    ]


def keep_accessible_urls(items: list[dict]) -> list[dict]:
    valid_items = []

    for item in items:
        url = item["url"]

        if is_url_accessible(url):
            valid_items.append(item)
        else:
            print(f"קישור לא תקין, מדלג: {url}")

    return valid_items


def main() -> None:
    sources = load_sources()
    all_results = collect_tenders(sources)
    architecture_tenders = get_architecture_tenders(all_results)
    valid_tenders = keep_accessible_urls(architecture_tenders)
    items_to_send = add_date_found(valid_tenders)

    send_to_make(items_to_send)

    print("\n======================")
    print(f"סה״כ נמצאו {len(all_results)} תוצאות")
    print(f"מכרזים רלוונטיים לאדריכלות: {len(architecture_tenders)}")
    print(f"מכרזים עם קישור תקין: {len(valid_tenders)}")
    print("======================\n")

    for item in valid_tenders:
        print(f"{item['city']} | {item['source']}")
        print(item["title"])
        print(item["url"])
        print("-" * 50)


if __name__ == "__main__":
    main()
