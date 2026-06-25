import re
from pathlib import Path
from urllib.parse import quote
from urllib.parse import unquote, urlparse


def encode_url(url: str) -> str:
    return quote(url, safe=":/?&=#%")


def title_from_url(url: str) -> str:
    path = urlparse(url).path
    filename = Path(unquote(path)).stem

    title = filename.replace("-", " ")
    title = title.replace("_", " ")
    title = " ".join(title.split())

    return title


def extract_tender_number(text: str) -> str:
    match = re.search(r"\b\d{2,3}[- ]\d{2}\b", text)

    if not match:
        return ""

    return match.group().replace(" ", "-")
