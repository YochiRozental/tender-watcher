import json

from src.scraper import scan_source


def load_candidate_sources() -> list[dict]:
    with open("candidate_sources.json", "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    sources = load_candidate_sources()

    for source in sources:
        print("\n======================")
        print(source["name"])
        print(source["url"])

        try:
            results = scan_source(source)
            print(f"עובד. נמצאו {len(results)} תוצאות.")
        except Exception as error:
            print(f"לא עובד: {error}")


if __name__ == "__main__":
    main()
