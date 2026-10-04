# Project Proposal: AI Women Safety Assistant

## Problem
Women face harassment, stalking and assault in public and private spaces. Existing apps
rely on manual panic buttons and do not assess risk proactively.

## Objectives
1. One-tap SOS with live location to trusted contacts.
2. Proactive risk scoring from time, location and situational cues.
3. Voice-distress detection to trigger help hands-free.
4. Automatic emergency classification to prioritise response.

## Proposed Solution
React front end, FastAPI back end, modular AI services (risk, voice, emergency classifier),
SQL database, SMS notification layer.

## Methodology
Requirements -> design -> iterative development -> testing with simulated scenarios -> evaluation.

## Expected Outcomes
Faster alerts, fewer missed emergencies, and a foundation for ML-based upgrades
(e.g. Whisper speech recognition, trained text classifiers, crime-heatmap integration).

## Risks & Ethics
Privacy of location data, false alarms, consent of contacts, data encryption. The app is not a
replacement for emergency services.

## Future Work
Wearable integration, offline mode, multilingual support, police API integration, ML model training.

## v2 Additions
- Multilingual voice emergency detection (English, Urdu, Sindhi, Roman Urdu/Sindhi).
- AI situation analyzer fusing text, context and audio cues into a threat level with localised guidance.
- Cancellable auto-SOS, per-contact SMS language, live-location tracking link, "I'm safe" confirmation.
