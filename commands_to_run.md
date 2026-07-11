# Commands to run this project

This file is a quick reference for setting up and running the project locally.

## 1) Prerequisites

Make sure these are installed first:

- Python 3.12+
- Git
- Ollama

### macOS
If Python is not installed yet, install it with Homebrew:

```bash
brew install python
```

If Ollama is not installed yet, install it with Homebrew:

```bash
brew install ollama
```

### Windows
Install Python from https://www.python.org/downloads/ and Ollama from https://ollama.com/download.

---

## 2) Open the project folder

```bash
cd /Users/hara/dev/GitHub/payment_rca_ai
```

---

## 3) Create and activate a virtual environment

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 4) Install Python dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

---

## 5) Start Ollama

Open a new terminal and run:

```bash
ollama serve
```

Keep this terminal running.

---

## 6) Pull the required Ollama models

In another terminal (while Ollama is running), run:

```bash
ollama pull nomic-embed-text
ollama list
```

Note:
- This project uses the embedding model: nomic-embed-text
- You do not need to pull llama3.2 for this setup unless your friend’s version of the project requires it

---

## 7) Build the local vector database / index

```bash
python -m src.rag.ingest
```

This step reads the CSV/HTML data and creates the local Chroma index.

---

## 8) Start the API server

```bash
uvicorn src.api.main:app --host 127.0.0.1 --port 8000
```

---

## 9) Test the API

In a browser or terminal, open:

```bash
http://127.0.0.1:8000/health
```

Or use:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"UP","service":"payment-ai-platform","version":"1.0.0"}
```

---

## Troubleshooting

### If you see an error about a missing model

```bash
ollama pull nomic-embed-text
```

### If the server does not start

Make sure Ollama is running first:

```bash
ollama serve
```

### If dependencies fail to install

Try:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```
