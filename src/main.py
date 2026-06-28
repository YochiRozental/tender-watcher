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


def collect_tenders(sources: list[dict]) -> tuple[list[dict], int, int]:
    all_results = []
    successful_sources = 0
    failed_sources = 0

    for source in sources:
        try:
            results = scan_source(source)
            print(f"{source['name']}: נמצאו {len(results)} תוצאות")
            all_results.extend(results)
            successful_sources += 1

        except Exception as error:
            failed_sources += 1
            print(f"שגיאה במקור {source['name']}: {error}")

    return all_results, successful_sources, failed_sources


def get_architecture_tenders(items: list[dict]) -> list[dict]:
    results = []
    seen_keys = set()

    for item in items:
        if not item.get("architecture_related"):
            continue

        url = item.get("url")
        if not url:
            continue

        tender_number = item.get("tender_number", "").strip()
        city = item.get("city", "").strip()
        title = item.get("title", "").strip()

        if tender_number:
            key = f"{city}|{tender_number}"
        else:
            key = url

        if key in seen_keys:
            continue

        seen_keys.add(key)
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
        url = item.get("url")

        if not url:
            print(f"פריט בלי קישור, מדלג: {item}")
            continue

        if is_url_accessible(url):
            valid_items.append(item)
        else:
            print(f"קישור לא תקין, מדלג: {url}")

    return valid_items


def print_summary(
        all_results: list[dict],
        architecture_tenders: list[dict],
        valid_tenders: list[dict],
        successful_sources: int,
        failed_sources: int,
        send_summary: dict,
) -> None:
    print("\n======================")
    print("סיכום ריצה יומית")
    print("======================")
    print(f"מקורות שנסרקו בהצלחה: {successful_sources}")
    print(f"מקורות שנכשלו: {failed_sources}")
    print(f"סה״כ נמצאו {len(all_results)} תוצאות")
    print(f"מכרזים רלוונטיים לאדריכלות: {len(architecture_tenders)}")
    print(f"מכרזים עם קישור תקין: {len(valid_tenders)}")
    print(f"נשלחו ל־Make בהצלחה: {send_summary['sent']}")
    print(f"נכשלו בשליחה ל־Make: {send_summary['failed']}")
    print("======================\n")


def print_tenders(items: list[dict]) -> None:
    for item in items:
        print(f"{item['city']} | {item['source']}")
        print(item["title"])
        print(item["url"])
        print("-" * 50)


def main() -> None:
    sources = load_sources()

    all_results, successful_sources, failed_sources = collect_tenders(sources)

    if successful_sources == 0:
        raise RuntimeError("כל המקורות נכשלו. יש לבדוק חיבור אינטרנט / חסימות / כתובות מקורות.")

    architecture_tenders = get_architecture_tenders(all_results)
    valid_tenders = keep_accessible_urls(architecture_tenders)
    items_to_send = add_date_found(valid_tenders)

    send_summary = send_to_make(items_to_send)

    print_summary(
        all_results=all_results,
        architecture_tenders=architecture_tenders,
        valid_tenders=valid_tenders,
        successful_sources=successful_sources,
        failed_sources=failed_sources,
        send_summary=send_summary,
    )

    print_tenders(valid_tenders)


if __name__ == "__main__":
    main()
