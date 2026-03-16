from typing import Any, Dict

import joblib
import pickle

from utils import highlight_suspicious_words, message_heuristics, sanitize_text


class MessageDetector:
    def __init__(self, model_path: str):
        try:
            self.model = joblib.load(model_path)
        except Exception:
            with open(model_path, "rb") as f:
                self.model = pickle.load(f)

    def predict(self, message: str) -> Dict[str, Any]:
        cleaned = sanitize_text(message)
        proba = float(self.model.predict_proba([cleaned])[0][1])
        label = "PHISHING" if proba >= 0.5 else "BENIGN"
        return {
            "probability": proba,
            "label": label,
            "heuristics": message_heuristics(cleaned),
            "highlight_terms": highlight_suspicious_words(cleaned),
        }


def analyze_message(message: str, model_path: str) -> Dict[str, Any]:
    detector = MessageDetector(model_path)
    return detector.predict(message)
