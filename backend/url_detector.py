import base64
import json
import os
from typing import Any, Dict, Optional

import joblib
import pickle
import requests

from utils import extract_url_features, sanitize_url


class URLDetector:
    def __init__(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)
        self.feature_order = [
            "url_length",
            "num_subdomains",
            "num_special_chars",
            "has_ip",
            "suspicious_tld",
            "keyword_hits",
            "uses_https",
        ]

    def predict(self, url: str) -> Dict[str, Any]:
        features = extract_url_features(url)
        vector = [[features[name] for name in self.feature_order]]
        proba = float(self.model.predict_proba(vector)[0][1])
        label = "PHISHING" if proba >= 0.5 else "BENIGN"
        return {
            "features": features,
            "probability": proba,
            "label": label,
        }


def _vt_url_id(url: str) -> str:
    url_bytes = url.encode("utf-8")
    return base64.urlsafe_b64encode(url_bytes).decode("utf-8").strip("=")


def query_virustotal(url: str, api_key: Optional[str]) -> Dict[str, Any]:
    url = sanitize_url(url)
    if not api_key:
        return {"status": "skipped", "reason": "VT_API_KEY missing"}
    url_id = _vt_url_id(url)
    headers = {"x-apikey": api_key}
    endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
    try:
        response = requests.get(endpoint, headers=headers, timeout=10)
        if response.status_code != 200:
            return {"status": "error", "code": response.status_code, "body": response.text[:200]}
        data = response.json()
        stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
        results = data.get("data", {}).get("attributes", {}).get("last_analysis_results", {})
        malicious = int(stats.get("malicious", 0))
        suspicious = int(stats.get("suspicious", 0))
        harmless = int(stats.get("harmless", 0))
        vendor_flags = sum(1 for v in results.values() if v.get("category") in {"malicious", "suspicious"})
        return {
            "status": "ok",
            "malicious": malicious,
            "suspicious": suspicious,
            "harmless": harmless,
            "vendor_flags": vendor_flags,
        }
    except Exception as exc:
        return {"status": "error", "reason": str(exc)}


def analyze_url(url: str, model_path: str, api_key: Optional[str]) -> Dict[str, Any]:
    detector = URLDetector(model_path)
    ml_result = detector.predict(url)
    vt_result = query_virustotal(url, api_key)
    return {
        "ml": ml_result,
        "virustotal": vt_result,
    }
