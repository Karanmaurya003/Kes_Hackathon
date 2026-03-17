import base64
import io
import json
import os
import re
import shutil
import sqlite3
import time
import urllib.parse
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

try:
    from PIL import Image
except Exception:
    Image = None

try:
    import pytesseract
except Exception:
    pytesseract = None
SUSPICIOUS_TLDS = {
    "ru",
    "tk",
    "ml",
    "ga",
    "cf",
    "gq",
    "cn",
    "biz",
    "top",
    "xyz",
    "info",
    "icu",
    "work",
    "zip",
}

BRAND_KEYWORDS = [
    "paypal",
    "microsoft",
    "google",
    "apple",
    "amazon",
    "bank",
    "secure",
    "login",
    "verify",
    "support",
    "account",
    "update",
]

PHISHING_MESSAGE_KEYWORDS = [
    "verify",
    "urgent",
    "suspended",
    "suspend",
    "confirm",
    "password",
    "bank",
    "account",
    "security",
    "locked",
    "unusual",
    "immediately",
    "click",
    "link",
    "payment",
    "refund",
    "invoice",
    "delivery",
    "prize",
]


def sanitize_text(text: str) -> str:
    cleaned = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", text or "")
    return cleaned.strip()


def sanitize_url(url: str) -> str:
    url = (url or "").strip()
    if not url:
        return ""
    if not re.match(r"^https?://", url, re.IGNORECASE):
        url = f"http://{url}"
    return url


def extract_domain(url: str) -> Tuple[str, str, str]:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.split("@")[-1].split(":")[0].lower()
    if not host:
        return "", "", ""
    parts = host.split(".")
    if len(parts) < 2:
        return host, host, ""
    tld = parts[-1]
    sld = parts[-2]
    subdomain = ".".join(parts[:-2]) if len(parts) > 2 else ""
    return host, f"{sld}.{tld}", subdomain


def has_ip_address(host: str) -> bool:
    if not host:
        return False
    return bool(re.match(r"^\d{1,3}(\.\d{1,3}){3}$", host))


def count_special_chars(url: str) -> int:
    return len(re.findall(r"[^a-zA-Z0-9]", url))


def extract_url_features(url: str) -> Dict[str, float]:
    url = sanitize_url(url)
    host, root_domain, subdomain = extract_domain(url)
    tld = root_domain.split(".")[-1] if root_domain else ""
    num_subdomains = 0 if not subdomain else len(subdomain.split("."))
    keyword_hits = sum(1 for k in BRAND_KEYWORDS if k in url.lower())
    return {
        "url_length": float(len(url)),
        "num_subdomains": float(num_subdomains),
        "num_special_chars": float(count_special_chars(url)),
        "has_ip": float(has_ip_address(host)),
        "suspicious_tld": float(tld in SUSPICIOUS_TLDS),
        "keyword_hits": float(keyword_hits),
        "uses_https": float(url.lower().startswith("https://")),
    }


def message_heuristics(message: str) -> Dict[str, float]:
    msg = sanitize_text(message).lower()
    keyword_hits = sum(1 for k in PHISHING_MESSAGE_KEYWORDS if k in msg)
    contains_link = float(bool(re.search(r"https?://|www\.", msg)))
    urgency = float(bool(re.search(r"urgent|immediately|asap|now", msg)))
    authority = float(bool(re.search(r"bank|security|admin|support|microsoft|paypal", msg)))
    emotion = float(bool(re.search(r"prize|won|congratulations|suspend|locked", msg)))
    return {
        "keyword_hits": float(keyword_hits),
        "contains_link": contains_link,
        "urgency": urgency,
        "authority": authority,
        "emotion": emotion,
    }


def highlight_suspicious_words(message: str) -> List[str]:
    msg = sanitize_text(message).lower()
    hits = [k for k in PHISHING_MESSAGE_KEYWORDS if k in msg]
    return sorted(set(hits))


def ensure_db(db_path: str) -> None:
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                url TEXT,
                message TEXT,
                risk_score REAL,
                risk_level TEXT,
                sources TEXT,
                payload TEXT
            )
            """
        )
        conn.commit()


def log_scan(db_path: str, url: str, message: str, risk_score: float, risk_level: str, sources: List[str], payload: Dict[str, Any]) -> int:
    ensure_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO scans (timestamp, url, message, risk_score, risk_level, sources, payload)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.utcnow().isoformat(),
                url,
                message,
                risk_score,
                risk_level,
                json.dumps(sources),
                json.dumps(payload),
            ),
        )
        conn.commit()
        return cur.lastrowid


def fetch_history(db_path: str, limit: int = 50) -> List[Dict[str, Any]]:
    ensure_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT * FROM scans ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [dict(row) for row in rows]


def summarize_trends(history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    buckets: Dict[str, Dict[str, int]] = {}
    for item in history:
        ts = item.get("timestamp") or ""
        day = ts.split("T")[0] if "T" in ts else ts[:10]
        if not day:
            continue
        if day not in buckets:
            buckets[day] = {"SAFE": 0, "SUSPICIOUS": 0, "HIGH RISK": 0}
        level = item.get("risk_level") or "SAFE"
        if level not in buckets[day]:
            buckets[day][level] = 0
        buckets[day][level] += 1
    series = []
    for day in sorted(buckets.keys()):
        entry = {"date": day}
        entry.update(buckets[day])
        series.append(entry)
    return series


def base64_to_bytes(data_url: str) -> Optional[bytes]:
    if not data_url:
        return None
    match = re.match(r"^data:.*?;base64,(.*)$", data_url)
    if not match:
        return None
    try:
        return base64.b64decode(match.group(1))
    except Exception:
        return None


def ocr_screenshot(data_url: str) -> Dict[str, Any]:
    if not data_url:
        return {"status": "skipped", "text": ""}
    if Image is None or pytesseract is None:
        return {"status": "error", "text": "", "reason": "OCR dependencies missing"}
    tesseract_cmd = os.getenv("TESSERACT_CMD") or shutil.which("tesseract")
    if not tesseract_cmd:
        candidates = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        ]
        for path in candidates:
            if os.path.exists(path):
                tesseract_cmd = path
                break
    if not tesseract_cmd:
        return {"status": "error", "text": "", "reason": "tesseract_not_found"}
    try:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    except Exception:
        return {"status": "error", "text": "", "reason": "Invalid Tesseract path"}
    raw = base64_to_bytes(data_url)
    if not raw:
        return {"status": "error", "text": "", "reason": "Invalid image data"}
    try:
        img = Image.open(io.BytesIO(raw))  # type: ignore[name-defined]
        img = img.convert("L")
        text = pytesseract.image_to_string(img, config="--psm 6")
        return {"status": "ok", "text": sanitize_text(text)}
    except Exception as exc:
        return {"status": "error", "text": "", "reason": str(exc)}

