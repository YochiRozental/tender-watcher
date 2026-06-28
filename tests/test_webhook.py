import os
import requests
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("MAKE_WEBHOOK_URL")

payload = {
    "date_found": "2026-06-24",
    "city": "בני ברק",
    "source": "עיריית בני ברק - מכרזים",
    "title": "מכרז 133-26 לקבלת שירותי תכנון ויועץ מיזוג אויר",
    "url": "https://example.com/tender.pdf",
    "source_page_url": "https://www.bnei-brak.muni.il/",
    "tender_number": "133-26",
    "architecture_related": True,
    "safe_url": "https://example.com/tender.pdf",
}

if not WEBHOOK_URL:
    raise RuntimeError("MAKE_WEBHOOK_URL is missing")

if __name__ == "__main__":
    response = requests.post(WEBHOOK_URL, json=payload, timeout=30)

    print(response.status_code)
    print(response.text)