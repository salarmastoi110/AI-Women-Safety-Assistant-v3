"""Voice distress detection.

1. Multilingual transcript analysis (browser Web Speech API / Whisper -> text).
2. Optional loudness analysis of 16-bit PCM WAV (scream-like spikes), stdlib only.
"""
import io
import math
import struct
import wave
from typing import Dict, Optional
from ai.common.lexicon import find_matches, detect_language


def analyze_transcript(text: str) -> Dict:
    m = find_matches(text)
    n_distress = sum(m.get("distress", {}).values())
    n_threat = sum(sum(m[c].values()) for c in ("assault", "stalking", "harassment", "medical", "accident") if c in m)
    score = min(1.0, 0.35 * n_distress + 0.45 * n_threat)
    keywords = [k for c in m if c != "danger" for k in m[c]]
    return {"distress_score": round(score, 2), "keywords": keywords, "language": detect_language(text)}


def _rms(samples) -> float:
    return math.sqrt(sum(s * s for s in samples) / len(samples)) if samples else 0.0


def analyze_wav(data: bytes) -> Dict:
    try:
        with wave.open(io.BytesIO(data), "rb") as w:
            width, rate, ch = w.getsampwidth(), w.getframerate(), w.getnchannels()
            frames = w.readframes(w.getnframes())
    except Exception as exc:
        return {"error": f"Unsupported audio: {exc}", "distress_score": 0.0}
    if width != 2:
        return {"error": "Only 16-bit PCM WAV supported", "distress_score": 0.0}
    count = len(frames) // 2
    samples = struct.unpack("<%dh" % count, frames[: count * 2])
    win = max(1, int(rate * 0.25)) * ch
    levels = [_rms(samples[i:i + win]) for i in range(0, len(samples), win)]
    if not levels:
        return {"distress_score": 0.0, "peak_rms": 0, "mean_rms": 0}
    peak, mean = max(levels), sum(levels) / len(levels)
    spike = (peak / mean) if mean else 0
    score = (0.4 if peak / 32768.0 > 0.3 else 0) + (0.3 if spike > 3 else 0)
    return {"distress_score": round(min(1.0, score), 2), "peak_rms": round(peak, 1),
            "mean_rms": round(mean, 1), "spike_ratio": round(spike, 2)}


def detect_distress(transcript: str = "", wav_bytes: Optional[bytes] = None) -> Dict:
    t = analyze_transcript(transcript)
    a = analyze_wav(wav_bytes) if wav_bytes else {"distress_score": 0.0}
    combined = min(1.0, t["distress_score"] + a.get("distress_score", 0.0))
    return {"distress_detected": combined >= 0.5, "combined_score": round(combined, 2),
            "transcript_analysis": t, "audio_analysis": a}
