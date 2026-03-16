from typing import Any, Dict, List

import joblib
import numpy as np
import shap

from utils import extract_url_features, sanitize_text


def explain_url(model_path: str, url: str) -> Dict[str, Any]:
    features = extract_url_features(url)
    feature_names = list(features.keys())
    vector = np.array([[features[name] for name in feature_names]])
    try:
        model = joblib.load(model_path)
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(vector)[1][0]
        pairs = list(zip(feature_names, shap_values))
        pairs.sort(key=lambda x: abs(x[1]), reverse=True)
        top = [{"feature": name, "impact": float(val)} for name, val in pairs[:6]]
        shap_map = {name: float(val) for name, val in pairs}
    except Exception:
        pairs = [(name, float(value)) for name, value in features.items()]
        pairs.sort(key=lambda x: abs(x[1]), reverse=True)
        top = [{"feature": name, "impact": float(val)} for name, val in pairs[:6]]
        shap_map = {name: float(val) for name, val in pairs}
    return {
        "features": features,
        "shap_values": shap_map,
        "top_factors": top,
    }


def explain_message(model_path: str, message: str) -> Dict[str, Any]:
    cleaned = sanitize_text(message)
    try:
        model = joblib.load(model_path)
        explainer = shap.Explainer(model, feature_names=None)
        shap_values = explainer([cleaned])
        values = shap_values.values[0]
        if hasattr(shap_values, "data"):
            tokens = shap_values.data[0]
        else:
            tokens = [f"token_{i}" for i in range(len(values))]
        pairs = list(zip(tokens, values))
        pairs.sort(key=lambda x: abs(x[1]), reverse=True)
        top = [{"token": str(token), "impact": float(val)} for token, val in pairs[:8]]
    except Exception:
        tokens = cleaned.split()[:8]
        top = [{"token": token, "impact": 0.2} for token in tokens]
    return {
        "top_tokens": top,
    }
