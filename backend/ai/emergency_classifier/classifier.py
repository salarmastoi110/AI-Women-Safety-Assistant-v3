"""Multilingual emergency classifier (EN / UR / SD / Roman)."""
from typing import Dict
from ai.common.lexicon import find_matches, detect_language

PRIORITY = {"assault": 1, "medical": 1, "stalking": 2, "harassment": 2, "accident": 2, "distress": 2, "other": 3}
CATS = ["assault", "medical", "stalking", "harassment", "accident"]


def classify_emergency(text: str) -> Dict:
    m = find_matches(text)
    lang = detect_language(text)
    scored = {c: sum(m[c].values()) for c in CATS if c in m}
    if scored:
        best = max(scored, key=lambda c: (scored[c], -PRIORITY[c]))
        return {"category": best, "priority": PRIORITY[best],
                "confidence": round(min(0.95, 0.5 + 0.15 * scored[best]), 2),
                "matched": list(m[best]), "language": lang}
    if "distress" in m:
        n = sum(m["distress"].values())
        return {"category": "distress", "priority": PRIORITY["distress"],
                "confidence": round(min(0.9, 0.4 + 0.15 * n), 2), "matched": list(m["distress"]), "language": lang}
    return {"category": "other", "priority": PRIORITY["other"], "confidence": 0.3, "matched": [], "language": lang}
