"""AI situation analyzer: fuses text (EN/UR/SD/Roman), context and optional audio into one verdict."""
from typing import Dict, Optional
from ai.common.lexicon import find_matches, detect_language
from ai.emergency_classifier.classifier import classify_emergency
from ai.risk_detection.detector import assess_risk
from ai.voice_detection.detector import analyze_transcript
from ai.situation_analyzer.messages import CATEGORY, LEVEL, SUMMARY, SUMMARY_CALM, ACTIONS, pick

BASE = {"assault": 55, "medical": 50, "accident": 40, "stalking": 35, "harassment": 30, "distress": 30}


def analyze_situation(text: str = "", hour: Optional[int] = None, is_alone: bool = False,
                      location_risk: Optional[float] = None, speed_kmh: Optional[float] = None,
                      audio_score: float = 0.0, ui_lang: str = "en") -> Dict:
    cls = classify_emergency(text)
    risk = assess_risk(hour=hour, message=text, location_risk=location_risk, is_alone=is_alone, speed_kmh=speed_kmh)
    voice = analyze_transcript(text)
    m = find_matches(text)

    category = cls["category"]
    hits = sum(sum(v.values()) for c, v in m.items() if c != "danger")
    distress_hits = sum(m.get("distress", {}).values())

    score = 0
    if category in BASE:
        score = BASE[category] + min(20, 8 * max(0, hits - 1))
        score += round(0.35 * risk["score"]) + round(30 * audio_score)
    else:
        score = round(0.35 * risk["score"]) + round(30 * audio_score)
    score = int(min(100, score))
    level = "critical" if score >= 85 else "high" if score >= 55 else "medium" if score >= 30 else "low"

    emergency = category != "other" and (score >= 55 or category in ("assault", "medical") or distress_hits >= 2)
    if audio_score >= 0.7 and category != "other":
        emergency = True

    actions_t = pick(ACTIONS, ui_lang)
    actions = []
    if emergency or level in ("medium", "high", "critical"):
        actions.append(actions_t["calm"])
    if emergency:
        actions.append(actions_t["alerting"])
    if category in ("assault", "medical", "accident") or level == "critical":
        actions.append(actions_t["emergency"])
    if category == "stalking":
        actions.append(actions_t["stalking"])
    if category == "harassment":
        actions.append(actions_t["harassment"])

    cat_label = pick(CATEGORY, ui_lang)[category]
    lvl_label = pick(LEVEL, ui_lang)[level]
    summary = (pick(SUMMARY, ui_lang).format(category=cat_label, level=lvl_label, score=score)
               if category != "other" else pick(SUMMARY_CALM, ui_lang))

    return {
        "language_detected": detect_language(text),
        "category": category, "category_label": cat_label,
        "priority": cls["priority"], "confidence": cls["confidence"],
        "threat_score": score, "level": level, "level_label": lvl_label,
        "emergency": emergency, "auto_trigger": emergency,
        "matched": cls["matched"], "voice": voice, "risk": risk,
        "summary": summary, "actions": actions,
    }
