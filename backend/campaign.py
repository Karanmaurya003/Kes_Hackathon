from typing import Any, Dict, List

from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer


def detect_campaigns(items: List[Dict[str, Any]], max_clusters: int = 3) -> List[Dict[str, Any]]:
    messages = [item.get("message") or "" for item in items if item.get("message")]
    urls = [item.get("url") or "" for item in items if item.get("url")]
    corpus = messages + urls
    if len(corpus) < 3:
        return []
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(corpus)
    n_clusters = min(max_clusters, max(2, len(corpus) // 2))
    model = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
    labels = model.fit_predict(X)
    campaigns = {}
    for idx, label in enumerate(labels):
        key = f"campaign_{label}"
        campaigns.setdefault(key, {"items": [], "count": 0})
        campaigns[key]["items"].append(corpus[idx])
        campaigns[key]["count"] += 1
    return [
        {"campaign_id": key, "count": val["count"], "sample": val["items"][:3]}
        for key, val in campaigns.items()
    ]

