from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from filters import (
    is_tender,
    is_architecture_related,
)
from utils import title_from_url, extract_tender_number


def scan_source(source: dict) -> list[dict]:
    print(f"\nבודק מקור: {source['name']}")

    response = requests.get(
        source["url"],
        timeout=30,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    results = []
    seen_urls = set()

    for link in soup.find_all("a"):
        title = link.get_text(" ", strip=True)
        href = link.get("href")

        if not title or not href:
            continue

        full_url = urljoin(
            source["url"],
            href,
        )
        clean_title = title

        if (
                title.lower() == "מסמכי המכרז"
                or title.lower() == "קישור לתשלום"
        ):
            clean_title = title_from_url(full_url)
        if full_url in seen_urls:
            continue

        search_text = f"{clean_title} {full_url}"

        if not is_tender(search_text):
            continue

        seen_urls.add(full_url)

        results.append(
            {
                "city": source["city"],
                "source": source["name"],
                "title": clean_title,
                "url": full_url,
                "tender_number": extract_tender_number(clean_title),
                "architecture_related": is_architecture_related(search_text),
            }
        )

    return results
