import os
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator

from domain_intelligence import analyze_domain
from explainability import explain_message, explain_url
from message_detector import analyze_message
from risk_engine import compute_risk_score, recommend_actions
from url_detector import analyze_url
from campaign import detect_campaigns
from utils import (
    base64_to_bytes,
    fetch_history,
    sanitize_text,
    sanitize_url,
    summarize_trends,
    log_scan,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "models")
URL_MODEL = os.path.join(MODEL_DIR, "url_model.pkl")
MSG_MODEL = os.path.join(MODEL_DIR, "message_model.pkl")
DB_PATH = os.path.join(BASE_DIR, "data", "phishlens.db")

app = FastAPI(title="PHISHLENS AI", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ThreatInput(BaseModel):
    url: Optional[str] = Field(default=None, description="URL to analyze")
    message: Optional[str] = Field(default=None, description="Message/email/SMS to analyze")
    screenshot: Optional[str] = Field(default=None, description="Base64 data URL screenshot")

    @validator("url")
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        cleaned = sanitize_url(v)
        if len(cleaned) > 2048:
            raise ValueError("URL too long")
        return cleaned

    @validator("message")
    def validate_message(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        cleaned = sanitize_text(v)
        if len(cleaned) > 5000:
            raise ValueError("Message too long")
        return cleaned


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze")
def analyze(payload: ThreatInput) -> Dict[str, Any]:
    if not payload.url and not payload.message:
        raise HTTPException(status_code=400, detail="Provide a URL or message to analyze.")

    vt_api_key = os.getenv("VT_API_KEY")
    url_result = analyze_url(payload.url, URL_MODEL, vt_api_key) if payload.url else None
    msg_result = analyze_message(payload.message, MSG_MODEL) if payload.message else None
    domain_result = analyze_domain(payload.url) if payload.url else None

    vt_stats = url_result.get("virustotal") if url_result else None
    url_ml = url_result.get("ml") if url_result else None

    score, level, sources = compute_risk_score(
        url_ml, msg_result, domain_result, vt_stats
    )

    response = {
        "input": payload.dict(),
        "url_analysis": url_result,
        "message_analysis": msg_result,
        "domain_intelligence": domain_result,
        "explainability": {
            "url": explain_url(URL_MODEL, payload.url) if payload.url else None,
            "message": explain_message(MSG_MODEL, payload.message) if payload.message else None,
        },
        "risk": {
            "score": score,
            "level": level,
        },
        "recommendations": recommend_actions(level),
    }

    log_scan(
        DB_PATH,
        payload.url or "",
        payload.message or "",
        score,
        level,
        sources,
        response,
    )

    return response


@app.get("/history")
def history(limit: int = 50) -> Dict[str, Any]:
    data = fetch_history(DB_PATH, limit=limit)
    return {"items": data}


@app.get("/trends")
def trends(limit: int = 120) -> Dict[str, Any]:
    data = fetch_history(DB_PATH, limit=limit)
    series = summarize_trends(data)
    return {"series": series}


@app.get("/simulate")
def simulate() -> Dict[str, Any]:
    samples = [
        "Your bank account will be suspended. Verify immediately using this link.",
        "Package delivery failed. Confirm your address to avoid return.",
        "Security alert: unusual sign-in. Reset your password now.",
    ]
    return {"samples": samples}


@app.get("/campaigns")
def campaigns(limit: int = 50) -> Dict[str, Any]:
    data = fetch_history(DB_PATH, limit=limit)
    return {"campaigns": detect_campaigns(data)}
