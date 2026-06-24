import csv
from datetime import date
from pathlib import Path

CSV_FILE = Path("tenders.csv")


def export_new_tenders(items: list[dict]) -> None:
    if not items:
        return

    file_exists = CSV_FILE.exists()

    with open(CSV_FILE, "a", encoding="utf-8-sig", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "date_found",
                "city",
                "source",
                "title",
                "url",
                "tender_number",
            ],
        )

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
