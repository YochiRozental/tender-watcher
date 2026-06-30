from src.constants import (
    TENDER_KEYWORDS,
    ARCHITECTURE_STRONG_KEYWORDS,
    ARCHITECTURE_GOOD_KEYWORDS,
    EXCLUDE_KEYWORDS,
    NON_PLANNING_EXCLUDE_KEYWORDS,
    PLANNING_KEYWORDS,
)


def normalize_text(text: str) -> str:
    return (text or "").replace("״", '"').replace("׳", "'").strip()


def contains_any(text: str, keywords: list[str]) -> bool:
    text = normalize_text(text)

    return any(
        keyword in text
        for keyword in keywords
    )


def is_tender(text: str) -> bool:
    return contains_any(text, TENDER_KEYWORDS)


def has_strong_architecture_keyword(text: str) -> bool:
    return contains_any(text, ARCHITECTURE_STRONG_KEYWORDS)


def has_good_architecture_keyword(text: str) -> bool:
    return contains_any(text, ARCHITECTURE_GOOD_KEYWORDS)


def has_exclude_keyword(text: str) -> bool:
    return contains_any(text, EXCLUDE_KEYWORDS)


def has_planning_keyword(text: str) -> bool:
    return contains_any(text, PLANNING_KEYWORDS)


def is_architecture_related(text: str) -> bool:
    text = normalize_text(text)

    strong_match = has_strong_architecture_keyword(text)
    good_match = has_good_architecture_keyword(text)
    planning_match = has_planning_keyword(text)
    excluded = has_exclude_keyword(text)
    non_planning = contains_any(text, NON_PLANNING_EXCLUDE_KEYWORDS)

    if strong_match:
        return True

    if excluded or non_planning:
        return False

    if planning_match and good_match:
        return True

    return False
