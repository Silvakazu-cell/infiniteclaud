import json
import os
from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()
BASE = Path(os.path.expanduser("~/.claude/automation"))


def _load(name):
    p = BASE / "analytics" / name
    return json.loads(p.read_text()) if p.exists() and p.stat().st_size > 2 else {}


@router.get("/api/analytics/metrics")
def get_metrics():
    data = _load("metrics.json")
    if not data:
        return {"message": "Nenhuma métrica ainda. Execute o collector."}
    return data


@router.get("/api/analytics/config")
def get_config():
    return _load("config.json")


@router.get("/api/analytics/suggestions")
def get_suggestions():
    data = _load("suggestions.json")
    return data if data else {"suggestions": [], "dismissed": []}


@router.get("/analytics")
def analytics_page():
    html_path = BASE / "dashboard/static/analytics.html"
    return HTMLResponse(html_path.read_text())
