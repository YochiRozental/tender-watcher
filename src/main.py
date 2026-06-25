import json

from src.config import SOURCES_FILE
from src.scraper import scan_source
from src.notifier import send_to_make


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


def main() -> None:
    sources = load_sources()
    all_results = collect_tenders(sources)
    architecture_tenders = get_architecture_tenders(all_results)

    send_to_make(architecture_tenders)

    print("\n======================")
    print(f"סה״כ נמצאו {len(all_results)} תוצאות")
    print(f"מכרזים רלוונטיים לאדריכלות: {len(architecture_tenders)}")
    print("======================\n")

    for item in architecture_tenders:
        print(f"{item['city']} | {item['source']}")
        print(item["title"])
        print(item["url"])
        print("-" * 50)


if __name__ == "__main__":
    main()