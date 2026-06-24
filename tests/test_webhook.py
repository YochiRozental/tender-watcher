import requests

WEBHOOK_URL = "https://hook.us1.make.com/227hgqrziy3g5yqece18jshnxedwi74m"

payload = {
    "date_found": "2026-06-24",
    "city": "בני ברק",
    "source": "עיריית בני ברק - מכרזים",
    "title": "מכרז 133-26 לקבלת שירותי תכנון ויועץ מיזוג אויר",
    "url": "https://example.com/tender.pdf",
    "tender_number": "133-26",
}

response = requests.post(WEBHOOK_URL, json=payload, timeout=30)

print(response.status_code)
print(response.text)
