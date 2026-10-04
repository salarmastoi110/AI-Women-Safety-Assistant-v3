from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form
from app.models import schemas
from ai.risk_detection.detector import assess_risk
from ai.voice_detection.detector import detect_distress, analyze_transcript
from ai.emergency_classifier.classifier import classify_emergency
from ai.situation_analyzer.analyzer import analyze_situation

router = APIRouter(prefix="/api", tags=["ai"])


@router.post("/analyze")
def analyze(data: schemas.AnalyzeIn):
    """Main endpoint: voice transcript (EN/UR/SD/Roman) -> full situation analysis."""
    return analyze_situation(text=data.text, hour=data.hour, is_alone=data.is_alone,
                             location_risk=data.location_risk, speed_kmh=data.speed_kmh,
                             audio_score=data.audio_score, ui_lang=data.lang)


@router.post("/risk/assess")
def risk(data: schemas.RiskIn):
    return assess_risk(**data.model_dump())


@router.post("/voice/analyze")
async def voice(transcript: str = Form(""), lang: str = Form("en"), audio: Optional[UploadFile] = File(None)):
    """Transcript + optional 16-bit WAV. Audio loudness is fused into the final analysis."""
    wav = await audio.read() if audio else None
    d = detect_distress(transcript, wav)
    analysis = analyze_situation(text=transcript, audio_score=d["audio_analysis"].get("distress_score", 0.0), ui_lang=lang)
    return {**d, "analysis": analysis}


@router.post("/voice/transcript")
def voice_transcript(data: schemas.VoiceIn):
    return {**analyze_transcript(data.transcript), "classification": classify_emergency(data.transcript)}
