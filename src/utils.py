import re
from pathlib import Path
from urllib.parse import quote, unquote, urlparse


def encode_url(url: str) -> str:
    return quote(url, safe=":/?&=#%")


def title_from_url(url: str) -> str:
    path = urlparse(url).path
    filename = Path(unquote(path)).stem

    title = filename.replace("-", " ")
    title = title.replace("_", " ")
    title = " ".join(title.split())

    return title


def is_pdf_url(url: str) -> bool:
    path = unquote(urlparse(url).path).lower()
    return path.endswith(".pdf")


def extract_tender_number(text: str) -> str:
    patterns = [
        r"\b\d{2,3}[- ]\d{2}\b",  # 133-26 / 133 26
        r"\b\d{1,3}/\d{4}\b",  # 13/2026
        r"\b\d{4}/\d{1,3}\b",  # 2026/13
        r"\b\d{1,3}[- ]\d{4}\b",  # 13-2026
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group().replace(" ", "-")

    return ""
