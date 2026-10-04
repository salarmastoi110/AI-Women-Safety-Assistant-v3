import os
from dotenv import load_dotenv

load_dotenv()
load_dotenv("../.env")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./safety.db")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")]
# Base URL contacts will open for live tracking (use your public/ngrok URL in real use)
PUBLIC_URL = os.getenv("PUBLIC_URL", "http://localhost:8000").rstrip("/")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_FROM_NUMBER = os.getenv("TWILIO_FROM_NUMBER", "")
