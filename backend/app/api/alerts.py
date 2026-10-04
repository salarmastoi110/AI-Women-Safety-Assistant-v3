from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import models, schemas
from app.models.database import get_db
from app.services import alert_service as svc

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.post("/sos", response_model=schemas.AlertOut)
def trigger_sos(data: schemas.SOSIn, db: Session = Depends(get_db)):
    return svc.to_out(svc.create_sos(db, data))


@router.get("", response_model=List[schemas.AlertOut])
def history(db: Session = Depends(get_db)):
    rows = db.query(models.Alert).order_by(models.Alert.id.desc()).limit(100).all()
    return [svc.to_out(a) for a in rows]


@router.post("/{token}/location", response_model=schemas.AlertOut)
def push_location(token: str, loc: schemas.LocationIn, db: Session = Depends(get_db)):
    a = svc.update_location(db, token, loc.latitude, loc.longitude)
    if not a:
        raise HTTPException(404, "Alert not found")
    return svc.to_out(a)


@router.post("/{token}/resolve", response_model=schemas.AlertOut)
def mark_safe(token: str, db: Session = Depends(get_db)):
    a = svc.resolve(db, token)
    if not a:
        raise HTTPException(404, "Alert not found")
    return svc.to_out(a)
