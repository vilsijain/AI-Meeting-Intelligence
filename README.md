# AI Meeting Intelligence Platform

A minimal end-to-end web app that extracts actionable insights from meeting recordings. Users can upload audio/video files and receive structured information about action items, decisions, and participant interactions.

## Tech Stack
- **Frontend:** React (Vite) + Tailwind CSS
- **Backend:** Python FastAPI
- **Database:** SQLite (via SQLModel)
- **AI Components:**
  - **Whisper.cpp** for transcription (CLI)
  - **Ollama** for LLM 
  - **ChromaDB** for vector search

> This starter works out of the box for the app skeleton and API. Transcription and LLM calls expect local services (Whisper.cpp, Ollama) to be installed and running. The code includes graceful fallbacks for when those services are unavailable so you can still demo the UI/API.

---

## Quick Start

### 0) Prereqs
- Python 3.10+
- Node 18+
- (Optional) Whisper.cpp binary installed locally (`main`) and a GGML model (e.g., `ggml-base.en.bin`)
- (Optional) Ollama installed and running: https://ollama.com/ (default host: `http://localhost:11434`)
- The code uses ChromaDB in local persistent mode (stores under `./backend/chroma_store`).

### 1) Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# (optional) set env vars
cp .env.example .env   # then edit paths if needed

# run API
uvicorn app:app --reload --port 8000
```

### 2) Frontend
```bash
cd ../frontend
npm install
npm run dev  # starts Vite dev server, usually on http://localhost:5173
```

### 3) Try it
- Open the frontend URL, upload an audio/video file.
- Or use curl to test:
```bash
curl -F "file=@sample.wav" http://localhost:8000/api/upload
```

---

## Configuration

Create `backend/.env` (copy from `.env.example`) to point to your local tools:

```
WHISPER_CPP_BIN=./whisper/main
WHISPER_CPP_MODEL=./whisper/models/ggml-base.en.bin
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3
```

If Whisper.cpp or Ollama are not available, the backend falls back to stub behavior so you can still see end-to-end flow.

---

## Architecture Decisions

See `docs/TECHNICAL_WRITEUP.md` for:
1. Architecture decisions
2. AI pipeline implementation
3. Challenges and solutions
4. Evaluation criteria
5. Code quality and organization
6. API design
7. AI/ML pipeline implementation
8. Error handling
9. Documentation

---

## Project Structure

```
ai-meeting-intel/
  backend/
    app.py
    models.py
    schemas.py
    db.py
    crud.py
    extract.py
    transcription.py
    llm.py
    search.py
    requirements.txt
    .env.example
    chroma_store/           # created at runtime
    media/                  # uploaded files
  frontend/
    index.html
    package.json
    vite.config.js
    postcss.config.js
    tailwind.config.js
    src/
      main.jsx
      App.jsx
      api.js
      components/
        FileUpload.jsx
        Dashboard.jsx
        MeetingList.jsx
        ActionItems.jsx
        Analytics.jsx
        SearchBar.jsx
  docs/
    TECHNICAL_WRITEUP.md
  scripts/
    seed_demo.py
  README.md
```

---
# Testing Approach

Unit Tests: Individual function and component testing
Integration Tests: API endpoint and database interaction
E2E Tests: Full user workflow testing (Cypress)
Performance Tests: Load testing with large files
AI Pipeline Tests: Transcription and analysis accuracy

## Docker

You can add Docker later. This starter keeps things simple for fast iteration.
