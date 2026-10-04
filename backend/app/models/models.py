import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from app.models.database import Base


class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    relation = Column(String(50), default="")
    language = Column(String(5), default="en")   # language the SMS to this contact is written in
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(32), unique=True, index=True, default=lambda: uuid.uuid4().hex)
    user_name = Column(String(100), default="")
    message = Column(Text, default="")
    summary = Column(Text, default="")
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    category = Column(String(30), default="other")
    level = Column(String(10), default="low")
    priority = Column(Integer, default=3)
    risk_score = Column(Integer, default=0)
    language = Column(String(10), default="en")
    source = Column(String(10), default="manual")     # manual | voice
    status = Column(String(20), default="active")     # active | resolved
    notified = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
