import os
import random

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from pathlib import Path


def train_url_model(output_path: str) -> None:
    random.seed(42)
    np.random.seed(42)
    X = []
    y = []
    for _ in range(600):
        url_length = random.randint(20, 180)
        num_subdomains = random.randint(0, 5)
        num_special = random.randint(3, 30)
        has_ip = random.choice([0, 1])
        suspicious_tld = random.choice([0, 1])
        keyword_hits = random.randint(0, 5)
        uses_https = random.choice([0, 1])
        features = [
            url_length,
            num_subdomains,
            num_special,
            has_ip,
            suspicious_tld,
            keyword_hits,
            uses_https,
        ]
        score = (
            0.2 * (url_length / 180)
            + 0.2 * (num_subdomains / 5)
            + 0.2 * (num_special / 30)
            + 0.2 * has_ip
            + 0.3 * suspicious_tld
            + 0.2 * (keyword_hits / 5)
            - 0.1 * uses_https
        )
        label = 1 if score > 0.6 else 0
        X.append(features)
        y.append(label)

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=6,
        random_state=42,
    )
    model.fit(X, y)
    joblib.dump(model, output_path)


def train_message_model(output_path: str) -> None:
    phishing = [
        "Your bank account will be suspended verify immediately",
        "Urgent action required to reset your password now",
        "Unusual sign in detected click the link to secure",
        "Payment failed update your billing details",
        "Confirm your account to avoid suspension",
        "Security alert verify your login immediately",
        "You have won a prize click to claim",
        "Invoice overdue open the attachment now",
    ]
    benign = [
        "Lunch meeting rescheduled to 2pm tomorrow",
        "Your receipt is attached for your records",
        "Monthly newsletter and product updates",
        "Please review the agenda for the team call",
        "Your order has shipped and is on the way",
        "Thanks for your help on the project",
        "Happy birthday hope you have a great day",
        "Reminder about the dentist appointment next week",
    ]
    texts = phishing + benign
    labels = [1] * len(phishing) + [0] * len(benign)
    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2))),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )
    pipeline.fit(texts, labels)
    joblib.dump(pipeline, output_path)


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    train_url_model(str(base_dir / "url_model.pkl"))
    train_message_model(str(base_dir / "message_model.pkl"))
    print("Models trained.")

