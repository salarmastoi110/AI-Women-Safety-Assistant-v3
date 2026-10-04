import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import config
from app.models.database import Base, engine
from app.models import models  # noqa: F401  (register tables)
from app.api import contacts, alerts, ai, track

logging.basicConfig(level=logging.INFO)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Women Safety Assistant", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=config.CORS_ORIGINS,
                   allow_methods=["*"], allow_headers=["*"])

for r in (contacts.router, alerts.router, ai.router, track.router):
    app.include_router(r)


@app.get("/")
def root():
    return {"app": "AI Women Safety Assistant", "version": "2.0.0", "languages": ["en", "ur", "sd"], "docs": "/docs"}
