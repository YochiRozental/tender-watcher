from constants import (
    TENDER_KEYWORDS,
    ARCHITECTURE_KEYWORDS,
)


def contains_any(text: str, keywords: list[str]) -> bool:
    text = (text or "").strip()

    return any(
        keyword in text
        for keyword in keywords
    )


def is_tender(text: str) -> bool:
    return contains_any(text, TENDER_KEYWORDS)


def is_architecture_related(text: str) -> bool:
    return contains_any(text, ARCHITECTURE_KEYWORDS)
