"""Public live-tracking page that trusted contacts open from the SMS link."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from app.models import models
from app.models.database import get_db

router = APIRouter(tags=["track"])


@router.get("/api/track/{token}")
def track_data(token: str, db: Session = Depends(get_db)):
    a = db.query(models.Alert).filter(models.Alert.token == token).first()
    if not a:
        raise HTTPException(404, "Not found")
    return {"name": a.user_name, "status": a.status, "category": a.category, "level": a.level,
            "summary": a.summary, "latitude": a.latitude, "longitude": a.longitude,
            "updated_at": a.updated_at.isoformat() + "Z"}


PAGE = """<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Live SOS</title>
<style>
body{margin:0;font-family:system-ui,'Noto Naskh Arabic',sans-serif;background:#10173a;color:#fff}
header{padding:16px;background:#b3202e}header.safe{background:#2a7f72}
h1{margin:0;font-size:20px}main{padding:12px}iframe{width:100%;height:60vh;border:0;border-radius:12px;background:#222}
a.btn{display:block;margin:12px 0;padding:14px;border-radius:10px;background:#fff;color:#10173a;text-align:center;text-decoration:none;font-weight:700}
small{opacity:.8}
</style></head><body>
<header id="h"><h1 id="t">SOS · ایمرجنسی · ايمرجنسي</h1><small id="s">Loading…</small></header>
<main><iframe id="map" title="map"></iframe>
<a class="btn" id="open" target="_blank" rel="noopener">Open in Google Maps · نقشہ کھولیں</a>
<small id="u"></small></main>
<script>
const token = location.pathname.split("/").pop();
async function tick(){
  try{
    const d = await (await fetch("/api/track/"+token)).json();
    document.getElementById("t").textContent = (d.name||"") + (d.status==="resolved" ? " — SAFE ✅ محفوظ" : " — SOS 🚨");
    document.getElementById("h").className = d.status==="resolved" ? "safe" : "";
    document.getElementById("s").textContent = d.summary || "";
    if(d.latitude!=null){
      const q = d.latitude+","+d.longitude;
      document.getElementById("map").src = "https://maps.google.com/maps?q="+q+"&z=16&output=embed";
      document.getElementById("open").href = "https://maps.google.com/?q="+q;
    }
    document.getElementById("u").textContent = "Updated: " + new Date(d.updated_at).toLocaleString();
  }catch(e){ document.getElementById("s").textContent = "Offline…"; }
}
tick(); setInterval(tick, 8000);
</script></body></html>"""


@router.get("/track/{token}", response_class=HTMLResponse)
def track_page(token: str):
    return PAGE
