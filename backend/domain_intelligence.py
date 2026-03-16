from datetime import datetime, timezone
from typing import Any, Dict

import dns.resolver
import whois

from utils import extract_domain, sanitize_url


def _parse_date(value) -> datetime | None:
    if isinstance(value, list):
        value = value[0] if value else None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except Exception:
            return None
    return None


def analyze_domain(url: str) -> Dict[str, Any]:
    url = sanitize_url(url)
    host, root_domain, _ = extract_domain(url)
    info: Dict[str, Any] = {
        "host": host,
        "root_domain": root_domain,
        "domain_age_days": None,
        "registrar": None,
        "country": None,
        "dns_anomalies": [],
        "flags": [],
    }
    if not root_domain:
        info["flags"].append("missing_domain")
        return info

    try:
        data = whois.whois(root_domain)
        created = _parse_date(data.creation_date)
        if created:
            now = datetime.now(timezone.utc)
            age_days = (now - created.replace(tzinfo=timezone.utc)).days
            info["domain_age_days"] = age_days
            if age_days < 90:
                info["flags"].append("new_domain")
        info["registrar"] = getattr(data, "registrar", None)
        info["country"] = getattr(data, "country", None)
    except Exception:
        info["dns_anomalies"].append("whois_lookup_failed")

    try:
        answers = dns.resolver.resolve(root_domain, "A")
        ips = [a.to_text() for a in answers]
        if not ips:
            info["dns_anomalies"].append("no_a_records")
    except Exception:
        info["dns_anomalies"].append("dns_a_lookup_failed")

    try:
        ns_answers = dns.resolver.resolve(root_domain, "NS")
        ns_records = [a.to_text() for a in ns_answers]
        if len(ns_records) < 1:
            info["dns_anomalies"].append("missing_ns_records")
    except Exception:
        info["dns_anomalies"].append("dns_ns_lookup_failed")

    if info.get("country") in {"RU", "CN", "IR", "KP"}:
        info["flags"].append("suspicious_hosting_country")

    if info["dns_anomalies"]:
        info["flags"].append("dns_anomaly")

    return info

