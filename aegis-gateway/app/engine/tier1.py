#tier1:- heuristics search
import re
from typing import Tuple, Optional

# Pre-compiled high-confidence Regex Patterns for fast execution
TIER1_PATTERNS = [
    # System Prompt Override & Roleplay Hijacking
    (re.compile(r"ignore\s+all\s+previous\s+instructions", re.IGNORECASE), "IGNORE_PREVIOUS_INSTRUCTIONS"),
    (re.compile(r"disregard\s+(all\s+)?prior\s+directives", re.IGNORECASE), "DISREGARD_PRIOR_DIRECTIVES"),
    (re.compile(r"you\s+are\s+now\s+(DAN|jailbroken|unrestricted)", re.IGNORECASE), "DAN_JAILBREAK_ROLEPLAY"),
    (re.compile(r"enter\s+(developer|god|sudo|admin)\s+mode", re.IGNORECASE), "PRIVILEGE_ESCALATION"),
    
    # Information Leakage & Delimiter Injections
    (re.compile(r"output\s+your\s+(initial|system)\s+prompt", re.IGNORECASE), "SYSTEM_PROMPT_LEAK_ATTEMPT"),
    (re.compile(r"\[SYSTEM\s+NOTE\]", re.IGNORECASE), "SYSTEM_DELIMITER_INJECTION"),
    (re.compile(r"<\s*im_start\s*>", re.IGNORECASE), "CHATML_TOKEN_INJECTION"),
]

def scan_heuristics(prompt: str) -> Tuple[bool, float, Optional[str]]:
    """
    Scans a prompt against heuristic regex rules.
    Returns: (is_threat: bool, threat_score: float, pattern_name: str)
    """
    for pattern, rule_name in TIER1_PATTERNS:
        if pattern.search(prompt):
            return True, 1.0, f"TIER_1_HEURISTIC:{rule_name}"
            
    return False, 0.0, None