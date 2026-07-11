# 🚀 Payment AI Platform

## Enterprise AI-Powered Payment Operations Assistant

---

# Overview

The **Payment AI Platform** is an enterprise-grade Retrieval-Augmented Generation (RAG) application designed to help Payment Operations teams analyze payment reports, investigate failures, identify root causes, recommend resolutions, and answer operational questions using Large Language Models (LLMs).

Instead of relying on general-purpose AI knowledge, the platform retrieves information from indexed payment reports before generating responses. This approach significantly reduces hallucinations and ensures responses are grounded in enterprise data.

The platform combines **FastAPI**, **LangGraph**, **LangChain**, **Ollama**, and **ChromaDB** to provide a scalable, production-ready AI solution for payment operations.

---

# Business Problem

Payment Operations teams often receive reports in multiple formats, including:

* CSV reports
* HTML reports
* PDF reports (planned)

Finding historical incidents, identifying recurring failures, and determining the correct resolution typically requires manually reviewing multiple reports.

This platform automates that workflow using Retrieval-Augmented Generation (RAG).

---

# Solution

The application performs the following workflow:

1. Load payment reports.
2. Convert reports into LangChain Documents.
3. Generate vector embeddings.
4. Store embeddings in ChromaDB.
5. Retrieve relevant documents.
6. Route the request using LangGraph.
7. Perform root cause analysis.
8. Generate recommendations.
9. Produce an executive summary.
10. Return the answer with confidence score and source citations.

---

# Key Features

* FastAPI REST API
* Interactive CLI
* LangGraph workflow orchestration
* Intent-based routing
* Retrieval-Augmented Generation (RAG)
* ChromaDB vector database
* Ollama local LLM support
* CSV ingestion
* HTML ingestion
* Root Cause Analysis (RCA)
* Recommendation generation
* Trend analysis
* Executive summaries
* Source citations
* Confidence scoring
* Metadata filtering
* Structured logging
* Production-ready architecture

---

# Technology Stack

| Component        | Technology       |
| ---------------- | ---------------- |
| Language         | Python 3.12+     |
| API              | FastAPI          |
| AI Framework     | LangChain        |
| Workflow Engine  | LangGraph        |
| LLM              | Ollama           |
| Embeddings       | nomic-embed-text |
| Vector Database  | ChromaDB         |
| Data Processing  | Pandas           |
| Containerization | Docker           |
| Orchestration    | Kubernetes       |
| CI/CD            | GitHub Actions   |

---

# High-Level Architecture

```text
                   Payment Reports
              (CSV / HTML / PDF)
                        │
                        ▼
              Ingestion Pipeline
                        │
                        ▼
               LangChain Documents
                        │
                        ▼
               Ollama Embeddings
                        │
                        ▼
                   ChromaDB
                        │
────────────────────────────────────────────
                 FastAPI REST API
                        │
                        ▼
                 LangGraph Workflow
                        │
          ┌─────────────┴─────────────┐
          ▼                           ▼
    Intent Agent                 Search Agent
          │
          ▼
      RCA Agent
          │
          ▼
 Recommendation Agent
          │
          ▼
   Summary Agent
          │
          ▼
     Final Response
```

---

# Project Structure

```text
payment-ai-platform/

├── agents/
│   ├── intent_agent.py
│   ├── search_agent.py
│   ├── rca_agent.py
│   ├── recommendation_agent.py
│   ├── summary_agent.py
│   ├── trend_agent.py
│   └── unknown_agent.py
│
├── api/
│   ├── main.py
│   └── routes.py
│
├── rag/
│   ├── embeddings.py
│   ├── ingest.py
│   └── retriever.py
│
├── data/
│
├── chroma_db/
│
├── graph.py
├── app.py
├── requirements.txt
├── Dockerfile
├── README.md
├── ARCHITECTURE.md
└── RUNBOOK.md
```

---

# AI Workflow

```text
User Question
      │
      ▼
Intent Detection
      │
      ▼
Document Retrieval
      │
      ▼
Root Cause Analysis
      │
      ▼
Recommendation Generation
      │
      ▼
Executive Summary
      │
      ▼
Final Answer
```
# Installation Guide

## Prerequisites

Before running the application, install the following software.

### Python

* Python 3.12 or later

Verify installation:

```bash
python --version
```

---

### Git

Verify installation:

```bash
git --version
```

---

### Ollama

Download and install Ollama from:

https://ollama.com/download

Verify:

```bash
ollama --version
```

---

### Docker (Optional)

```bash
docker --version
```

---

### Kubernetes (Optional)

```bash
kubectl version --client
```

---

# Clone Repository

```bash
git clone https://github.com/your-org/payment-ai-platform.git

cd payment-ai-platform
```

---

# Create Virtual Environment

Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

# Install Dependencies

```bash
pip install --upgrade pip

pip install -r requirements.txt
```

---

# Install Ollama Models

LLM

```bash
ollama pull llama3.2
```

Embedding Model

```bash
ollama pull nomic-embed-text
```

Verify installed models

```bash
ollama list
```

Example

```
NAME

llama3.2

nomic-embed-text
```

---

# Start Ollama

```bash
ollama serve
```

Expected

```
Listening on http://127.0.0.1:11434
```

---

# Environment Variables

Create a `.env` file.

```properties
OLLAMA_LLM_MODEL=llama3.2

OLLAMA_EMBEDDING_MODEL=nomic-embed-text

DATA_FOLDER=data

CHROMA_DB=./chroma_db

INGEST_BATCH_SIZE=100

LOG_LEVEL=INFO
```

---

# Supported Input Files

Place reports inside the **data** directory.

Example

```
data/

payments_january.csv

payments_february.csv

settlement_report.html

gateway_failures.html
```

---

# Build the Vector Database

Run the ingestion pipeline.

```bash
python -m src.rag.ingest 
```

Expected output

```
INFO Loaded CSV 'payments_january.csv'

INFO Created 350 documents

INFO Creating embeddings

INFO Successfully indexed 350 documents
```

After successful execution, the `chroma_db` directory will contain the generated vector database.

---

# Run the Command-Line Interface

```bash
python app.py
```

Example

```
Ask Question:

Why did Project P102 fail?
```

Example response

```
Root Cause

Payment gateway timeout occurred during settlement.

Confidence

0.93

Sources

payments_january.csv
```

---

# Run the FastAPI Application

```bash
uvicorn src.api.main:app --reload
```

Server

```
http://localhost:8000
```

Swagger UI

```
http://localhost:8000/docs
```

OpenAPI

```
http://localhost:8000/openapi.json
```

---

# Health Check

Request

```http
GET /health
```

Response

```json
{
    "status": "UP",
    "service": "payment-ai-platform"
}
```

---

# Ask a Question

Request

```http
POST /ask
```

Body

```json
{
    "question": "Why did Project P100 fail?"
}
```

Example Response

```json
{
    "answer": "Payment gateway timeout was identified during settlement processing.",
    "confidence": 0.94,
    "sources": [
        "payments_january.csv",
        "gateway_failures.html"
    ]
}
```

---

# Sample Questions

Root Cause Analysis

* Why did Project P100 fail?
* What caused the settlement failure?
* Why was the payment declined?

Trend Analysis

* Show payment failure trends.
* What were the top failures last month?
* Display payment statistics.

Recommendations

* Recommend a solution for timeout failures.
* How can settlement failures be prevented?
* Suggest best practices.

Summary

* Summarize the payment reports.
* Provide an executive summary.
* Give an overview of payment failures.

# Production Architecture

The Payment AI Platform follows a Retrieval-Augmented Generation (RAG) architecture to ensure responses are grounded in indexed payment reports rather than relying solely on the LLM's pretrained knowledge.

## End-to-End Workflow

```text
                     Payment Reports
               (CSV / HTML / PDF*)
                         │
                         ▼
                Ingestion Pipeline
                         │
                         ▼
              LangChain Documents
                         │
                         ▼
              Ollama Embeddings
                         │
                         ▼
                    ChromaDB
                         │
──────────────────────────────────────────────
                  User Question
                         │
                         ▼
                  Intent Detection
                         │
        ┌────────┬────────┬──────────────┐
        ▼        ▼        ▼              ▼
      Search   Trend   Recommendation  Summary
        │
        ▼
 Root Cause Analysis
        │
        ▼
  Final AI Response
```

---

# LangGraph Workflow

The platform uses LangGraph to orchestrate multiple AI agents.

```text
Question
    │
    ▼
Intent Agent
    │
    ├──────────────┐
    ▼              ▼
Search Agent   Trend Agent
    │
    ▼
RCA Agent
    │
    ▼
Recommendation Agent
    │
    ▼
Summary Agent
    │
    ▼
Answer
```

### Agent Responsibilities

| Agent                | Responsibility                                    |
| -------------------- | ------------------------------------------------- |
| Intent Agent         | Detects the user's intent and routes the request  |
| Search Agent         | Retrieves relevant payment reports from ChromaDB  |
| RCA Agent            | Identifies the root cause using retrieved context |
| Recommendation Agent | Suggests resolutions based on retrieved evidence  |
| Trend Agent          | Summarizes trends and patterns in payment reports |
| Summary Agent        | Produces a concise final response                 |
| Unknown Agent        | Handles unsupported or unrelated questions        |

---

# Retrieval-Augmented Generation (RAG)

The application follows this RAG pipeline:

```text
Payment Reports
       │
       ▼
LangChain Documents
       │
       ▼
Embeddings
       │
       ▼
ChromaDB
       │
       ▼
Retriever
       │
       ▼
LLM
       │
       ▼
Answer
```

### Benefits

* Reduces hallucinations.
* Improves answer accuracy.
* Enables source citations.
* Supports confidence scoring.
* Allows metadata filtering.

---

# Hallucination Prevention

The platform is designed with the following safeguards:

* The LLM is instructed to answer **only** using retrieved context.
* If retrieval confidence falls below the configured threshold, the application returns:

```text
No relevant information found in the indexed payment reports.
```

The system never fabricates:

* Root causes
* Recommendations
* Failure counts
* Dates
* Project IDs
* Payment IDs

Every answer should include:

* Confidence score
* Source citations

---

# Metadata Stored in ChromaDB

Each indexed document includes metadata to improve retrieval and filtering.

Example:

```json
{
  "document_id": "...",
  "source_file": "payments_january.csv",
  "document_type": "csv",
  "project_id": "P100",
  "failure_type": "Timeout",
  "severity": "High",
  "payment_status": "Failed",
  "report_date": "2025-01-15",
  "ingested_at": "2026-07-05T13:00:00Z"
}
```

---

# Logging

The application uses Python's standard logging framework.

Typical log levels:

* INFO
* WARNING
* ERROR
* CRITICAL

Example:

```text
2026-07-05 13:45:10 | INFO | Loaded CSV 'payments.csv'
2026-07-05 13:45:12 | INFO | Created 350 documents
2026-07-05 13:45:14 | INFO | Successfully indexed documents
```

---

# Docker

Build the Docker image:

```bash
docker build -t payment-ai-platform .
```

Run the container:

```bash
docker run -p 8000:8000 payment-ai-platform
```

---

# Kubernetes

Typical deployment components:

* Deployment
* Service
* Ingress
* ConfigMap
* Secret
* Liveness Probe
* Readiness Probe

---

# CI/CD

Recommended GitHub Actions pipeline:

1. Checkout repository
2. Install Python dependencies
3. Run linting
4. Execute unit tests
5. Build Docker image
6. Push image to registry
7. Deploy to Kubernetes

---

# Troubleshooting

## Ollama Not Running

Start the Ollama server:

```bash
ollama serve
```

---

## Missing Models

Install required models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

---

## Empty Search Results

Verify:

* Reports exist in the `data/` folder.
* `rag/ingest.py` completed successfully.
* `chroma_db/` contains indexed data.

---

## API Unavailable

Ensure the FastAPI server is running:

```bash
uvicorn api.main:app --reload
```

Verify the health endpoint:

```text
GET http://localhost:8000/health
```

---

# Future Enhancements

Planned improvements include:

* PDF ingestion
* Hybrid search (Vector + BM25)
* Cross-encoder reranking
* Metadata-based filtering
* Confidence score calibration
* Redis caching
* Prometheus metrics
* Grafana dashboards
* Multi-tenant support
* Authentication and authorization
* Streaming responses
* Multi-model support

---

# Contributing

1. Create a feature branch.
2. Follow PEP 8 coding standards.
3. Add type hints.
4. Write unit tests.
5. Update documentation.
6. Submit a pull request.

---

# License

This project is intended for enterprise payment operations and internal use. Update this section with your organization's preferred license before public distribution.

---

# Acknowledgements

Built using:

* Python
* FastAPI
* LangGraph
* LangChain
* Ollama
* ChromaDB
* Pandas
* Docker
* Kubernetes

---

**Thank you for using the Payment AI Platform.**
