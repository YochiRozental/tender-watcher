import json

from scraper import scan_source
from storage import load_seen_urls, save_seen_urls

from exporter import export_new_tenders
def load_sources() -> list[dict]:
    with open(
        "sources.json",
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def main():
    sources = load_sources()

    all_results = []

    for source in sources:
        try:
            results = scan_source(source)
            print(f"נמצאו {len(results)} תוצאות")
            all_results.extend(results)

        except Exception as error:
            print(f"שגיאה במקור {source['name']}: {error}")

    already_seen_urls = load_seen_urls()

    architecture_results = []
    urls_found_this_run = set()

    for item in all_results:
        if not item["architecture_related"]:
            continue

        url = item["url"]

        if url in urls_found_this_run:
            continue

        urls_found_this_run.add(url)

        if url in already_seen_urls:
            continue

        architecture_results.append(item)

    updated_seen_urls = already_seen_urls | urls_found_this_run
    save_seen_urls(updated_seen_urls)
    export_new_tenders(architecture_results)

    print("\n======================")
    print(f"סה״כ נמצאו {len(all_results)} תוצאות")
    print(f"מכרזים חדשים רלוונטיים: {len(architecture_results)}")
    print("======================\n")

    for item in architecture_results:
        print(f"{item['city']} | {item['source']}")
        print(item["title"])
        print(item["url"])
        print("-" * 50)


if __name__ == "__main__":
    main()