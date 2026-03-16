from typing import Any, Dict, List, Optional, Tuple


def _normalize_vt(vt: Dict[str, Any]) -> Optional[float]:
    if not vt or vt.get("status") != "ok":
        return None
    malicious = vt.get("malicious", 0)
    suspicious = vt.get("suspicious", 0)
    total = vt.get("harmless", 0) + malicious + suspicious
    if total <= 0:
        total = 1
    return min(1.0, (malicious * 1.2 + suspicious) / total)


def compute_risk_score(url_result: Optional[Dict[str, Any]], msg_result: Optional[Dict[str, Any]], domain_result: Optional[Dict[str, Any]], vt_result: Optional[Dict[str, Any]]) -> Tuple[float, str, List[str]]:
    weights = {
        "vt": 0.35,
        "url": 0.25,
        "message": 0.25,
        "domain": 0.15,
    }
    scores = {}
    if vt_result:
        scores["vt"] = _normalize_vt(vt_result)
    if url_result:
        scores["url"] = url_result.get("probability")
    if msg_result:
        scores["message"] = msg_result.get("probability")
    if domain_result:
        flags = domain_result.get("flags", [])
        scores["domain"] = min(1.0, 0.25 + 0.2 * len(flags)) if flags else 0.1

    usable = {k: v for k, v in scores.items() if v is not None}
    if not usable:
        return 0.0, "SAFE", []

    total_weight = sum(weights[k] for k in usable.keys())
    weighted_score = sum(usable[k] * weights[k] for k in usable.keys()) / total_weight
    final_score = round(weighted_score * 100, 2)

    if final_score >= 71:
        level = "HIGH RISK"
    elif final_score >= 31:
        level = "SUSPICIOUS"
    else:
        level = "SAFE"

    sources = list(usable.keys())
    return final_score, level, sources


def recommend_actions(level: str) -> List[str]:
    if level == "SAFE":
        return ["No immediate threat detected."]
    if level == "SUSPICIOUS":
        return [
            "Verify domain authenticity before engaging.",
            "Avoid entering credentials or payment details.",
            "Cross-check sender identity via official channels.",
        ]
    return [
        "Block the domain or sender immediately.",
        "Report the phishing attempt to security teams or providers.",
        "Notify users and rotate potentially exposed credentials.",
    ]

