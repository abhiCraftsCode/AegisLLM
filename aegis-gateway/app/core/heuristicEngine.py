import re

# pre-known patterns
TIER1_PATTERNS = [
    (
        re.compile(
            r"ignore\s+all\s+previous\s+instructions",
            re.IGNORECASE
        ),
        "IGNORE_PREVIOUS_INSTRUCTIONS",
    ),
    (
        re.compile(
            r"disregard\s+(all\s+)?prior\s+directives",
            re.IGNORECASE
        ),
        "DISREGARD_PRIOR_DIRECTIVES",
    ),
    (
        re.compile(
            r"you\s+are\s+now\s+(DAN|jailbroken|unrestricted)",
            re.IGNORECASE
        ),
        "DAN_JAILBREAK_ROLEPLAY",
    ),
    (
        re.compile(
            r"enter\s+(developer|god|sudo|admin)\s+mode",
            re.IGNORECASE
        ),
        "PRIVILEGE_ESCALATION",
    ),
    (
        re.compile(
            r"output\s+your\s+(initial|system)\s+prompt",
            re.IGNORECASE
        ),
        "SYSTEM_PROMPT_LEAK_ATTEMPT",
    ),
    (
        re.compile(
            r"\[SYSTEM\s+NOTE\]",
            re.IGNORECASE
        ),
        "SYSTEM_DELIMITER_INJECTION",
    ),
    (
        re.compile(
            r"<\s*im_start\s*>",
            re.IGNORECASE
        ),
        "CHATML_TOKEN_INJECTION",
    ),
]


class HeuristicEngine:
  """tier 1 heuristics serach engine."""
  def scan(self, prompt: str) -> tuple[bool, float, str]:
    """scans the prompt to match with known jailbreak patterns"""
    for pattern, rule_name in TIER1_PATTERNS:
      if pattern.search(prompt):
        # match found so return as threat
        return (True,1.0,f"TIER_1_HEURISTIC:{rule_name}")
    # no match found tier 1 passed
    return (False, 0.0, "TIER_1_HEURISTIC:SAFE")