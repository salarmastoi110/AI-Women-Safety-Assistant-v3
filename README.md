# Hifazat · حفاظت — AI Women Safety Assistant (v2)

Voice-activated emergency detection for **English, Urdu (اردو) and Sindhi (سنڌي)** — including Roman Urdu/Sindhi
typed or transcribed text. When the AI hears an emergency, it counts down (cancellable), then sends an SMS with a
**live-location tracking link** to every trusted contact, each in *their* preferred language.

## How it works
```
Mic -> Web Speech API (ur-PK / sd-PK / en-US) -> transcript
     -> POST /api/analyze  (multilingual lexicon + context risk + optional audio loudness)
     -> verdict: category, threat score, level, recommended actions (in UI language)
     -> if emergency: 10s cancel countdown -> POST /api/alerts/sos
     -> SMS to contacts (their language) with /track/<token> link
     -> phone keeps pushing GPS every 15 s; contacts see it live; "I'm safe" notifies everyone
```

## Features
- Voice guard (continuous listening, auto-restart) + typed "test without speaking" box
- AI situation analyzer: assault, stalking, harassment, medical, accident, general distress
- Language detection: English / Urdu / Sindhi / Roman
- UI in English, اردو, سنڌي with full RTL layout
- Cancel countdown (5–30 s), vibration, manual SOS
- Live tracking page for contacts + "I'm safe" message
- Per-contact SMS language
- Emergency numbers (tap to call)

## Run
```bash
# backend
cd backend
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env .env
rm -f safety.db                                          # if upgrading from v1 (schema changed)
uvicorn app.main:app --reload --host 0.0.0.0

# frontend
cd frontend
npm install
npm run dev
```
Tests: `cd backend && pip install pytest && python -m pytest -q tests`

## Real SMS
`pip install twilio`, fill `TWILIO_*` and set `PUBLIC_URL` to a URL your contacts can reach
(deploy, or use ngrok). Without Twilio, SMS are simulated and printed in the server log.

## Important limitations
- Browser speech recognition (Chrome/Edge) needs internet. **Sindhi (`sd-PK`) recognition is not guaranteed in all
  browsers**; the app falls back to Urdu. Sindhi *text* is always analysed correctly.
- Voice guard works only while the page is open and the screen is on. A native mobile app is needed for background use.
- Detection is keyword/rule-based: it can miss emergencies and can false-alarm. That's why there is a cancel countdown.
- Check the emergency numbers in `frontend/services/i18n.js`, and have a native speaker review Urdu/Sindhi strings.
- Academic prototype — not a replacement for emergency services.

## Structure
```
frontend/   React + Vite (components, pages, services/i18n, assets)
backend/    FastAPI app + ai/ (common lexicon, voice_detection, risk_detection, emergency_classifier, situation_analyzer)
database/   SQL schema
docs/       Proposal & presentation
```
