import re
from datetime import datetime
from typing import List, Optional


def extract_regex_field(text: str, patterns: List[str]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def parse_date(date_str: str) -> Optional[datetime]:
    if not date_str:
        return None

    formats = [
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%d/%m/%y",
        "%d-%m-%y",
        "%Y-%m-%d",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue

    return None


def extract_section_text(
    text: str, header_pattern: str, stop_headers: List[str]
) -> Optional[str]:
    pattern = f"{header_pattern}[:\n](.*?)(?:{'|'.join(stop_headers)}|$)"
    match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
