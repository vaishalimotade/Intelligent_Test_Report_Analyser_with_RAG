# Intelligent Test Report Analyzer & Insights Engine

Enterprise-grade GenAI platform that ingests CI/CD test reports, detects flaky tests, analyzes recurring failure patterns, and produces automated quality digests.

## Overview

- Backend: FastAPI with PostgreSQL
- Frontend: React + Material UI
- AI/RAG: Azure OpenAI, LangChain, ChromaDB
- Ingestion: JUnit, Allure, Extent Reports from Jenkins, GitHub Actions, and manual uploads
- Notifications: Slack + Email
- Deployment: Docker, docker-compose, Kubernetes
- Tests: pytest coverage > 90%

## Directory Structure

- `backend/`: FastAPI application
- `frontend/`: React dashboard
- `ingestion/`: parsers and report upload utilities
- `analytics/`: flaky detection, failure pattern, heatmap
- `ai_engine/`: RAG pipeline, embeddings, root cause analysis
- `database/`: migrations and schema scripts
- `notification/`: Slack and email notifications
- `deployment/`: docker-compose, Kubernetes manifests
- `tests/`: unit and integration tests
- `docs/`: architecture and API docs

## Requirements

- Python 3.11
- Node 20+
- PostgreSQL
- Docker
- kubectl

## Setup

1. `cd intelligent-test-report-analyzer`
2. `docker compose up --build`
3. Open frontend at `http://localhost:3000`
4. Open backend docs at `http://localhost:8000/docs`

## Environment Variables

- `DATABASE_URL`
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `SLACK_WEBHOOK_URL`
- `EMAIL_SMTP_HOST`
- `EMAIL_SMTP_PORT`
- `EMAIL_SMTP_USER`
- `EMAIL_SMTP_PASSWORD`
- `NOTIFICATION_FROM_EMAIL`
- `NOTIFICATION_ADMIN_EMAIL`
- `CHROMADB_DIR`

## Key Features

- Report ingest via API and file upload
- Historical test repository with trend analysis
- Flakiness scoring and risk categorization
- Failure pattern clustering and module hotspot heatmap
- RAG-powered root cause analysis with Azure OpenAI
- Weekly quality digest generation in HTML, PDF, Slack, and email
- Enterprise-ready deployment with Docker and Kubernetes
