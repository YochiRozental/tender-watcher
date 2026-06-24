import json

from src.config import SOURCES_FILE
from src.exporter import export_new_tenders
from src.notifier import send_to_make
from src.scraper import scan_source
from src.storage import load_seen_urls, save_seen_urls


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


def get_new_architecture_tenders(items: list[dict]) -> list[dict]:
    already_seen_urls = load_seen_urls()
    urls_found_this_run = set()
    new_items = []

    for item in items:
        url = item["url"]

        urls_found_this_run.add(url)

        if not item["architecture_related"]:
            continue

        if url in already_seen_urls:
            continue

        if any(existing["url"] == url for existing in new_items):
            continue

        new_items.append(item)

    save_seen_urls(already_seen_urls | urls_found_this_run)

    return new_items


def main() -> None:
    sources = load_sources()
    all_results = collect_tenders(sources)
    new_tenders = get_new_architecture_tenders(all_results)

    export_new_tenders(new_tenders)
    send_to_make(new_tenders)

    print("\n======================")
    print(f"סה״כ נמצאו {len(all_results)} תוצאות")
    print(f"מכרזים חדשים רלוונטיים: {len(new_tenders)}")
    print("======================\n")

    for item in new_tenders:
        print(f"{item['city']} | {item['source']}")
        print(item["title"])
        print(item["url"])
        print("-" * 50)


if __name__ == "__main__":
    main()
