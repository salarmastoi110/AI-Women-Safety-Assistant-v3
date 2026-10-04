from datetime import datetime
from sqlalchemy.orm import Session
from app import config
from app.models import models, schemas
from app.services.notification_service import notify_each
from ai.situation_analyzer.analyzer import analyze_situation
from ai.situation_analyzer.messages import CATEGORY, LEVEL, SMS_SOS, SMS_SAFE, pick


def track_url(token: str) -> str:
    return f"{config.PUBLIC_URL}/track/{token}"


def to_out(a: models.Alert) -> schemas.AlertOut:
    out = schemas.AlertOut.model_validate(a)
    out.track_url = track_url(a.token)
    return out


def create_sos(db: Session, data: schemas.SOSIn) -> models.Alert:
    # Manual SOS always counts as an emergency; voice SOS was already analysed on the client.
    res = analyze_situation(text=data.message, hour=data.hour, is_alone=data.is_alone, ui_lang=data.lang)
    category = res["category"] if res["category"] != "other" else "distress"
    level = res["level"] if data.source == "voice" else max(res["level"], "high", key=["low", "medium", "high", "critical"].index)

    alert = models.Alert(
        user_name=data.user_name, message=data.message, summary=res["summary"],
        latitude=data.latitude, longitude=data.longitude, category=category, level=level,
        priority=res["priority"] if res["category"] != "other" else 2, risk_score=res["threat_score"],
        language=res["language_detected"], source=data.source,
    )
    db.add(alert); db.commit(); db.refresh(alert)

    name = data.user_name or "—"
    link = track_url(alert.token)
    msgs = []
    for c in db.query(models.Contact).all():
        lang = c.language if c.language in ("en", "ur", "sd") else "en"
        body = pick(SMS_SOS, lang).format(
            name=name, category=pick(CATEGORY, lang)[category], level=pick(LEVEL, lang)[level], link=link)
        msgs.append((c.phone, body))
    alert.notified = notify_each(msgs)
    db.commit(); db.refresh(alert)
    return alert


def update_location(db: Session, token: str, lat: float, lng: float):
    a = db.query(models.Alert).filter(models.Alert.token == token).first()
    if a and a.status == "active":
        a.latitude, a.longitude, a.updated_at = lat, lng, datetime.utcnow()
        db.commit(); db.refresh(a)
    return a


def resolve(db: Session, token: str):
    a = db.query(models.Alert).filter(models.Alert.token == token).first()
    if not a:
        return None
    if a.status != "resolved":
        a.status, a.updated_at = "resolved", datetime.utcnow()
        msgs = []
        for c in db.query(models.Contact).all():
            lang = c.language if c.language in ("en", "ur", "sd") else "en"
            msgs.append((c.phone, pick(SMS_SAFE, lang).format(name=a.user_name or "—")))
        notify_each(msgs)
        db.commit(); db.refresh(a)
    return a
