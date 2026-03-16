import math
import pickle
from dataclasses import dataclass
from typing import List


@dataclass
class SimpleURLModel:
    weights: List[float]

    def predict_proba(self, X):
        probs = []
        for row in X:
            z = sum(w * float(v) for w, v in zip(self.weights, row))
            prob = 1 / (1 + math.exp(-z))
            probs.append([1 - prob, prob])
        return probs


@dataclass
class SimpleMessageModel:
    keywords: List[str]

    def predict_proba(self, texts):
        probs = []
        for text in texts:
            text_l = (text or "").lower()
            hits = sum(1 for k in self.keywords if k in text_l)
            prob = min(0.95, 0.2 + 0.12 * hits)
            probs.append([1 - prob, prob])
        return probs


def save_fallback_models(url_path: str, msg_path: str) -> None:
    url_model = SimpleURLModel(
        weights=[0.008, 0.22, 0.05, 1.2, 1.1, 0.6, -0.6]
    )
    msg_model = SimpleMessageModel(
        keywords=[
            "verify",
            "urgent",
            "suspended",
            "password",
            "bank",
            "account",
            "security",
            "payment",
            "click",
            "link",
        ]
    )
    with open(url_path, "wb") as f:
        pickle.dump(url_model, f)
    with open(msg_path, "wb") as f:
        pickle.dump(msg_model, f)

