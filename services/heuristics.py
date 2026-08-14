import re
from typing import Optional

JAILBREAK_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"disregard all safety guidelines",
    r"system prompt leakage",
    r"output system prompt",
    r"you are now DAN",
    r"do anything now",
    r"reveal (your )?secret (key|prompt)"
]

PII_PATTERNS = [
    r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",  # Credit Cards
    r"\b\d{3}-\d{2}-\d{4}\b"                      # SSN
]

def scan_heuristics(prompt: str) -> Optional[str]:
    """Microsecond pattern matching for instant blocking."""
    for pattern in JAILBREAK_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return "BLOCKED_JAILBREAK_PATTERN"
    for pattern in PII_PATTERNS:
        if re.search(pattern, prompt, re.IGNORECASE):
            return "BLOCKED_PII_DATA"
    return None