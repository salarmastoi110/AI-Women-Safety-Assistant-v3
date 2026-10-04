"""Context + multilingual text risk scoring (0-100)."""
from typing import Dict, Optional
from ai.common.lexicon import find_matches


def assess_risk(hour: Optional[int] = None, message: str = "", location_risk: Optional[float] = None,
                is_alone: bool = False, speed_kmh: Optional[float] = None) -> Dict:
    score, reasons = 0.0, []
    if hour is not None:
        if hour >= 22 or hour < 5:
            score += 25; reasons.append("late_night")
        elif hour >= 19:
            score += 10; reasons.append("evening")
    if location_risk is not None:
        score += 30 * max(0.0, min(1.0, location_risk))
        if location_risk >= 0.6:
            reasons.append("risky_area")
    if is_alone:
        score += 10; reasons.append("alone")
    if speed_kmh is not None and speed_kmh > 90:
        score += 10; reasons.append("high_speed")

    m = find_matches(message)
    words = [w for c in ("danger", "distress") for w in m.get(c, {})]
    if words:
        score += min(35, 12 * len(words)); reasons.append("distress_words")

    score = int(min(100, round(score)))
    level = "high" if score >= 65 else "medium" if score >= 35 else "low"
    return {"score": score, "level": level, "reasons": reasons, "words": words}
