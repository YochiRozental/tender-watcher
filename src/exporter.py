import csv
from datetime import date

from src.config import CSV_FILE

FIELDNAMES = [
    "date_found",
    "city",
    "source",
    "title",
    "url",
    "tender_number",
]


def export_new_tenders(items: list[dict]) -> None:
    if not items:
        return

    CSV_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)

        if not file_exists:
            writer.writeheader()

        for item in items:
            writer.writerow({
                "date_found": date.today().isoformat(),
                "city": item["city"],
                "source": item["source"],
                "title": item["title"],
                "url": item["url"],
                "tender_number": item.get("tender_number", ""),
            })
