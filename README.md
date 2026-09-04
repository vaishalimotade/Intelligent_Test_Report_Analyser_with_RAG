# Intelligent Test Report Analyzer & Insights Engine

Enterprise-grade GenAI platform that ingests CI/CD test reports, detects flaky tests, analyzes recurring failure patterns, and produces automated quality digests.

## Overview

- Backend: FastAPI with MongoDB
- Frontend: Streamlit dashboard (Python virtual environment)
- Optional frontend: React dashboard (Node.js/npm)
- AI/RAG: OpenAI, LangChain, ChromaDB
- Ingestion: JUnit, Allure, Extent Reports from Jenkins, GitHub Actions, and manual uploads
- Notifications: Slack + Email
- Deployment: local processes or Kubernetes
- Tests: pytest coverage > 90%

## Directory Structure

- `backend/`: FastAPI application
- `frontend/`: React dashboard
- `streamlit/`: Streamlit upload and dashboard application
- `ingestion/`: parsers and report upload utilities
- `analytics/`: flaky detection, failure pattern, heatmap
- `ai_engine/`: RAG pipeline, embeddings, root cause analysis
- `database/`: migrations and schema scripts
- `notification/`: Slack and email notifications
- `deployment/`: Kubernetes manifests
- `tests/`: unit and integration tests
- `docs/`: architecture and API docs

## Requirements

- Python 3.11
- Node 20+
- MongoDB
- MongoDB 7+

## Setup

1. `cd intelligent-test-report-analyzer`
2. Start MongoDB locally on `mongodb://localhost:27017`, or use an approved MongoDB Atlas URL.
3. Create the backend environment: `py -3.11 -m venv backend\\.venv`
4. Create the frontend environment: `py -3.11 -m venv streamlit\\.venv`
5. Copy `backend\\.env.example` to `backend\\.env` and add backend secrets.
6. Copy `streamlit\\.env.example` to `streamlit\\.env`.
7. Install backend dependencies: `backend\\.venv\\Scripts\\python.exe -m pip install -r backend/requirements.txt`
8. Install frontend dependencies: `streamlit\\.venv\\Scripts\\python.exe -m pip install -r streamlit/requirements.txt`
9. Start FastAPI: `cd backend` then `..\\backend\\.venv\\Scripts\\python.exe -m uvicorn app.main:app --reload --port 8000`
10. In another terminal, start Streamlit: `streamlit\\.venv\\Scripts\\python.exe -m streamlit run streamlit/streamlit_app.py`
11. Open Streamlit at `http://localhost:8501` and backend docs at `http://localhost:8000/docs`

### Local environment files

The official Python setup uses separate environment files:

```powershell
Copy-Item backend\.env.example backend\.env
Copy-Item streamlit\.env.example streamlit\.env
notepad backend\.env
notepad streamlit\.env
```

The backend `.env` contains API keys, database credentials, Slack webhooks, SMTP credentials, and RAG settings. The Streamlit `.env` contains only the backend URL. Both files are ignored by git. Restart FastAPI and Streamlit after changing them.

### Demo reports

`demo_reports.zip` contains three JUnit reports for builds 1, 2, and 3. Extract the archive, then upload the XML files one at a time while changing the build number in the sidebar to `1`, `2`, and `3`. This produces recurring errors and a pass/fail history for the flaky-test and hotspot demonstrations.

## Environment Variables

- `MONGODB_URL`
- `MONGODB_DATABASE`
- `OPENAI_API_KEY`
- `OPENAI_EMBEDDING_MODEL`
- `OPENAI_CHAT_MODEL`
- `OPENAI_MODEL`
- `OPENAI_BASE_URL`
- `SLACK_WEBHOOK_URL`
- `EMAIL_SMTP_HOST`
- `EMAIL_SMTP_PORT`
- `EMAIL_SMTP_USER`
- `EMAIL_SMTP_PASSWORD`
- `NOTIFICATION_FROM_EMAIL`
- `NOTIFICATION_ADMIN_EMAIL`
- `CHROMADB_DIR`
- `WEEKLY_DIGEST_SLACK_ENABLED` (default `true`)
- `WEEKLY_DIGEST_EMAIL_ENABLED` (default `false`)
- `WEEKLY_DIGEST_INTERVAL_SECONDS` (default `604800`; use a small value to test locally)

## Dashboard capabilities

The Streamlit dashboard supports multiple XML uploads, shared date/pipeline/feature filters, feature pass/fail percentages, test-case success distribution, grouped error categories, related runs and test cases, flaky-test identification across runs, and feature hotspots.

Failed records are indexed into Chroma during ingestion for historical root-cause retrieval. Chunking first keeps the test/error summary and technical stack trace together; oversized sections use recursive paragraph/line/word splitting with overlap. Set `CHROMADB_DIR`, `RAG_NAMESPACE`, and `RAG_CHUNK_MAX_CHARS` as needed, and configure `OPENAI_API_KEY` before uploading failures.

The FastAPI process starts the weekly digest loop automatically. For local testing, set `WEEKLY_DIGEST_INTERVAL_SECONDS=60`; enable delivery with `SLACK_WEBHOOK_URL` and/or the email SMTP variables. The loop waits for the interval before its first delivery and stops cleanly when FastAPI shuts down.

## Key Features

- Report ingest via API and file upload
- Historical test repository with trend analysis
- Flakiness scoring and risk categorization
- Failure pattern clustering and module hotspot heatmap
- RAG-powered root cause analysis with OpenAI
- Weekly quality digest generation in HTML, PDF, Slack, and email
- Enterprise-ready deployment with Docker and Kubernetes
