# PHISHLENS AI
Explainable Multi-Layer Phishing Detection Platform

## Overview
PHISHLENS AI is a hackathon-ready prototype that detects phishing threats across URLs, messages, and domain reputation with explainable AI. It combines ML classifiers, VirusTotal intelligence, and WHOIS/DNS signals into a single risk score with recommended actions.

## Architecture
Pipeline:
User Input → Threat Input Module → Feature Extraction → Detection Engines → Explainable AI → Risk Scoring → Response Recommendation → Dashboard

Architecture diagram: `architecture/system_diagram.png`

## Modules
1. Threat Input Module: input validation and sanitization.
2. URL Threat Detection: VirusTotal + URL ML classifier.
3. Message Phishing Detection: TF-IDF + Logistic Regression.
4. Domain Intelligence: WHOIS + DNS anomaly checks.
5. Explainable AI: SHAP feature contributions.
6. Risk Scoring Engine: weighted risk score (0–100).
7. Response Recommendation Engine: defensive playbooks.
8. Dashboard: interactive UI + charts.
9. Threat History Log: SQLite history.
10. Innovation: phishing simulation, risk trends, token highlighting.

## Backend API
Base URL: `http://localhost:8000`

### POST `/analyze`
Request:
```
{
  "url": "http://secure-paypal-verification.ru/login",
  "message": "Your bank account will be suspended. Verify immediately.",
  "screenshot": "data:image/png;base64,... (optional)"
}
```
Response:
```
{
  "risk": { "score": 88.2, "level": "HIGH RISK" },
  "recommendations": ["Block the domain..."],
  "url_analysis": {...},
  "message_analysis": {...},
  "domain_intelligence": {...},
  "explainability": {
    "url": {"top_factors": [...]},
    "message": {"top_tokens": [...]}
  }
}
```

### GET `/history`
Returns the last scans from SQLite.

### GET `/trends`
Returns aggregated risk trends by date.

### GET `/simulate`
Returns phishing simulation samples.

### GET `/campaigns`
Clusters recent messages/URLs into campaigns.

## Frontend
Next.js + TailwindCSS + Chart.js dashboard. The UI shows:
- risk score + level
- explainability charts
- highlighted suspicious message terms
- threat history
- trend analytics

## Local Setup
### Backend
```
cd phishlens-ai/backend
python -m pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Set environment variables:
```
setx VT_API_KEY "your_virustotal_key"
```

### Frontend
```
cd phishlens-ai/frontend
npm install
npm run dev
```
Optional API override:
```
setx NEXT_PUBLIC_API_URL "http://localhost:8000"
```

## Deployment
- Backend: Render (Docker or Python service).
- Frontend: Vercel (Next.js).
- Add `VT_API_KEY` as environment variable in backend deployment.

## Dataset Suggestions
- Phishing URL dataset: UCI Phishing Websites, PhishTank exports.
- Email/SMS phishing: Kaggle SMS Spam Collection, Enron email + phishing labels.
- Domain intel: OpenPhish feeds, CERT reports for malicious domains.

## Example Inputs
URL:
`http://secure-paypal-verification.ru/login`

Message:
`Your bank account will be suspended. Verify immediately.`

Expected Output:
- Risk score: 70+
- Risk level: HIGH RISK
- Explanation: suspicious TLD, keyword hits, urgent language.

## Model Notes
The `models/` directory contains lightweight fallback models for local demos. For fuller ML models:
```
python phishlens-ai/models/train_models.py
```
