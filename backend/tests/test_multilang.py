import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import os
os.environ["DATABASE_URL"] = "sqlite:///./test_safety.db"

from fastapi.testclient import TestClient
from ai.situation_analyzer.analyzer import analyze_situation
from ai.common.lexicon import detect_language

CASES = [
    ("someone is following me, please help", "en", "stalking", True),
    ("مجھے بچاؤ کوئی میرا پیچھا کر رہا ہے", "ur", "stalking", True),
    ("بچاؤ بچاؤ وہ مجھے مار رہا ہے", "ur", "assault", True),
    ("مون کي بچايو، ڪو منهنجي پٺيان پيو اچي", "sd", "stalking", True),
    ("مدد ڪريو، هو مون کي ماري رهيو آهي", "sd", "assault", True),
    ("mujhe bachao koi mera peecha kar raha hai", "roman", "stalking", True),
    ("bachao bachao madad karo", "roman", "distress", True),
    ("hello, how are you today", "en", "other", False),
    ("آج موسم بہت اچھا ہے", "ur", "other", False),
]


def test_cases():
    for text, lang, cat, trig in CASES:
        r = analyze_situation(text=text, hour=23, is_alone=True)
        assert detect_language(text) == lang, (text, detect_language(text))
        assert r["category"] == cat, (text, r["category"])
        assert r["auto_trigger"] == trig, (text, r["threat_score"], r["auto_trigger"])


def test_localised_output():
    ur = analyze_situation("بچاؤ مجھے مار رہا ہے", ui_lang="ur")
    sd = analyze_situation("بچاؤ مجھے مار رہا ہے", ui_lang="sd")
    assert "حملہ" in ur["summary"] and "حملو" in sd["summary"]


def test_api_flow():
    from app.main import app
    c = TestClient(app)
    c.post("/api/contacts", json={"name": "Ammi", "phone": "+921", "relation": "mother", "language": "ur"})
    c.post("/api/contacts", json={"name": "Bhai", "phone": "+922", "relation": "brother", "language": "sd"})
    r = c.post("/api/alerts/sos", json={"message": "مجھے بچاؤ", "latitude": 26.24, "longitude": 68.4,
                                         "hour": 23, "lang": "ur", "user_name": "Ayesha", "source": "voice"}).json()
    assert r["notified"] == 2 and r["track_url"].endswith(r["token"])
    r2 = c.post(f"/api/alerts/{r['token']}/location", json={"latitude": 26.3, "longitude": 68.5}).json()
    assert r2["latitude"] == 26.3
    assert c.get(f"/track/{r['token']}").status_code == 200
    assert c.get(f"/api/track/{r['token']}").json()["status"] == "active"
    assert c.post(f"/api/alerts/{r['token']}/resolve").json()["status"] == "resolved"
