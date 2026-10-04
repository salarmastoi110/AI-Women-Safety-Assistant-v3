from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ContactIn(BaseModel):
    name: str
    phone: str
    relation: str = ""
    language: str = "en"


class ContactOut(ContactIn):
    model_config = ConfigDict(from_attributes=True)
    id: int


class RiskIn(BaseModel):
    hour: Optional[int] = None
    message: str = ""
    location_risk: Optional[float] = None
    is_alone: bool = False
    speed_kmh: Optional[float] = None


class AnalyzeIn(BaseModel):
    text: str = ""
    hour: Optional[int] = None
    is_alone: bool = False
    location_risk: Optional[float] = None
    speed_kmh: Optional[float] = None
    audio_score: float = 0.0
    lang: str = "en"          # language of the UI / response


class SOSIn(BaseModel):
    message: str = ""
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hour: Optional[int] = None
    is_alone: bool = True
    lang: str = "en"
    user_name: str = ""
    source: str = "manual"


class LocationIn(BaseModel):
    latitude: float
    longitude: float


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    token: str
    user_name: str
    message: str
    summary: str
    latitude: Optional[float]
    longitude: Optional[float]
    category: str
    level: str
    priority: int
    risk_score: int
    language: str
    source: str
    status: str
    notified: int
    created_at: datetime
    updated_at: datetime
    track_url: str = ""


class VoiceIn(BaseModel):
    transcript: str = ""
