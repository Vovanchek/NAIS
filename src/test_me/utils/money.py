import re


def discount_for_subtotal(subtotal: int) -> int:
    return subtotal * 10 // 100


def format_uah(cents: int) -> str:
    hryvnias, remainder = divmod(cents, 100)
    return f"{hryvnias:,}".replace(",", " ") + f",{remainder:02d} грн"


def parse_uah(text: str) -> int:
    match = re.search(r"(\d[\d\s\u00a0]*),(\d{2})", text)
    if not match:
        raise ValueError(f"No UAH amount found in: {text!r}")
    whole = int(re.sub(r"\s|\u00a0", "", match.group(1)))
    return whole * 100 + int(match.group(2))
