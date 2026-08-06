# Expense Intelligence Platform

An end-to-end expense management and forecasting platform built with FastAPI, PostgreSQL (Supabase), and machine learning — covering automated expense categorization, time-series forecasting, and anomaly detection. Fully containerized with Docker and deployed via a GitHub Actions CI/CD pipeline to AWS EC2.

---

## Features

- **Expense Forecasting** — ARIMA-based time-series forecasting to predict future departmental spend, with safeguards against negative forecasts on sparse data.
- **Automated Categorization** — Logistic regression model to classify expenses into categories from transaction metadata.
- **Anomaly Detection** — Isolation Forest model to flag unusual or potentially fraudulent expense entries.
- **REST API** — FastAPI backend exposing endpoints for expense CRUD operations, forecasts, categorization, and anomaly flags.
- **Cloud-Native Deployment** — Dockerized application, pushed to Amazon ECR, and deployed on an EC2 instance via an automated CI/CD pipeline.

---

## Tech Stack

| Layer            | Technology |
|-------------------|------------|
| API Framework      | FastAPI |
| ORM / Database     | SQLAlchemy + PostgreSQL (Supabase) |
| ML — Forecasting   | ARIMA (statsmodels) |
| ML — Categorization| Logistic Regression (scikit-learn) |
| ML — Anomaly Detection | Isolation Forest (scikit-learn) |
| Containerization   | Docker |
| CI/CD              | GitHub Actions |
| Cloud Infrastructure | AWS EC2, Amazon ECR |

---

## Architecture

```
                ┌────────────────────┐
                │   GitHub Actions    │
                │   (CI Pipeline)     │
                └─────────┬───────────┘
                          │ build & push image
                          ▼
                ┌────────────────────┐
                │   Amazon ECR        │
                └─────────┬───────────┘
                          │ pull latest image
                          ▼
                ┌────────────────────┐
                │   AWS EC2 (t2.micro)│
                │   Docker Container   │
                │   - FastAPI App      │
                │   - ML Modules       │
                └─────────┬───────────┘
                          │ pooled connection
                          ▼
                ┌────────────────────┐
                │   Supabase (Postgres)│
                └────────────────────┘
```

---

## Project Structure

```
Company_expense_tracker/
├── app/
│   ├── main.py               # FastAPI entrypoint
│   ├── models/                # SQLAlchemy models
│   ├── routers/                # API route handlers
│   └── ml/
│       ├── forecasting.py     # ARIMA forecasting logic
│       ├── model_train.py     # Training pipeline for categorization
│       ├── model_predict.py   # Inference for categorization
│       └── anomaly.py         # Isolation Forest anomaly detection
├── .github/
│   └── workflows/
│       └── ci.yml              # CI pipeline (build, sanity checks)
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Docker
- A Supabase (PostgreSQL) project
- AWS account (for deployment)

### Local Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/Company_expense_tracker.git
cd Company_expense_tracker

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# then fill in your DB_* variables below
```

### Environment Variables

The app expects five separate `DB_*` variables (not a single `DATABASE_URL`):

```
DB_HOST=aws-1-ap-northeast-1.pooler.supabase.com
DB_PORT=6543
DB_NAME=postgres
DB_USER=your_supabase_user
DB_PASSWORD=your_supabase_password
```

### Run Locally

```bash
uvicorn app.main:app --reload
```

API docs available at `http://localhost:8000/docs`

---

## Running with Docker

```bash
# Build the image
docker build -t exp-track .

# Run the container
docker run -d -p 8000:8000 --env-file .env --restart unless-stopped exp-track
```

---

## Deployment (AWS EC2 + ECR)

1. Build and tag the Docker image, then push to ECR:
   ```bash
   docker tag exp-track:latest 128833123216.dkr.ecr.eu-north-1.amazonaws.com/exp-track:latest
   docker push 128833123216.dkr.ecr.eu-north-1.amazonaws.com/exp-track:latest
   ```
2. On the EC2 instance, pull and run the latest image:
   ```bash
   docker pull 128833123216.dkr.ecr.eu-north-1.amazonaws.com/exp-track:latest
   docker run -d -p 8000:8000 --env-file /home/ubuntu/.env --restart unless-stopped 128833123216.dkr.ecr.eu-north-1.amazonaws.com/exp-track:latest
   ```
3. GitHub Actions automates the build-and-push step on every push to `main` (**CI-only** — the pipeline runs import/sanity checks; deployment to EC2 is currently a manual pull step, not an automated CD step).

> **Note:** EC2 public IPs change on instance reboot. An Elastic IP is recommended to keep the deployment address stable.

---

## Machine Learning Modules

| Module | Purpose | Notes |
|--------|---------|-------|
| `forecasting.py` | ARIMA-based expense forecasting per department | Forecasts are clipped at zero (`.clip(lower=0)`) to handle sparse-data edge cases |
| `model_train.py` / `model_predict.py` | Logistic regression for expense categorization | Trained on historical labeled transactions |
| `anomaly.py` | Isolation Forest for anomaly/fraud flagging | DB engine initialization is scoped inside functions to avoid eager-execution issues during import |

---

## Known Design Decisions

- **Eager execution avoided**: All database engine/connection creation happens inside functions rather than at module import time, preventing CI import failures.
- **CI vs. CD**: The current GitHub Actions pipeline performs continuous integration (build, import checks) — it does not yet auto-deploy to EC2.
- **Elastic IP**: Strongly recommended for production use to avoid stale IP issues after instance restarts.

---

## Roadmap

- [ ] Apply Elastic IP to EC2 instance
- [ ] Extend CI pipeline to include automated pytest coverage
- [ ] Expand ML surface (e.g., additional models, explainability with SHAP/LIME)
- [ ] Add automated CD step for EC2 deployment

---
