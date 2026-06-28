from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from src.filters import (
    is_tender,
    is_architecture_related,
)
from src.utils import (
    title_from_url,
    extract_tender_number,
    is_pdf_url,
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

GENERIC_TITLES = {
    "מסמכי המכרז",
    "קישור לתשלום",
    "להורדה",
    "לחץ כאן",
    "פרטים נוספים",
    "מסמך",
    "pdf",
    "קובץ מצורף",
}


def is_tender_page_url(url: str) -> bool:
    lower_url = url.lower()

    return (
            "/bids/" in lower_url
            or "/gd_bids/" in lower_url
            or "michraz" in lower_url
            or "tender" in lower_url
            or "tenders" in lower_url
            or "מכרז" in url
    )


def get_context_text(link) -> str:
    parent = link.find_parent(["tr", "li", "article", "div"])
    if not parent:
        return ""

    return parent.get_text(" ", strip=True)


def scan_source(source: dict) -> list[dict]:
    print(f"\nבודק מקור: {source['name']}")

    response = requests.get(
        source["url"],
        timeout=30,
        headers=HEADERS,
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

        if not href:
            continue

        full_url = urljoin(
            source["url"],
            href,
        )

        clean_title = title.strip() if title else ""

        if not clean_title or clean_title.lower() in GENERIC_TITLES:
            clean_title = title_from_url(full_url)

        context_text = get_context_text(link)
        search_text = f"{clean_title} {context_text} {full_url}"

        is_pdf = is_pdf_url(full_url)
        is_tender_page = is_tender_page_url(full_url)

        if not is_pdf and not is_tender_page:
            continue

        if full_url in seen_urls:
            continue

        if not is_tender(search_text):
            continue

        seen_urls.add(full_url)

        results.append(
            {
                "city": source["city"],
                "source": source["name"],
                "title": clean_title,
                "url": full_url,
                "source_page_url": source["url"],
                "tender_number": extract_tender_number(search_text),
                "architecture_related": is_architecture_related(search_text),
            }
        )

    return results
