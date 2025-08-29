# AI Meeting Intelligence Platform

AI Meeting Intelligence Platform end-to-end web app that extracts  insights from meeting recordings. Users can upload audio/video files and receive information about action items, decisions, and participant interactions.

## Tech Stack
- **Frontend:** React (Vite) + Tailwind CSS
- **Backend:** Python FastAPI
- **Database:** SQLite (via SQLModel)
- **AI Components:**
  - **Whisper.cpp** for transcription (CLI)
  - **Ollama** for LLM 
  - **ChromaDB** for vector search

---

## Quick Start

### 1) Prereqs
- Python 3.10+
- Node 18+
- Whisper.cpp binary installed locally (`main`) and a GGML model 
- Ollama installed and running: https://ollama.com/default host
- The code uses ChromaDB in local persistent mode (stores under `./backend/chroma_store`).

### 2) Backend
```bash
cd backend
python -m venv .venv 
source .venv/bin/activate # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# run API
uvicorn app:app --reload --port 8000
```

### 3) Frontend
```bash
cd ../frontend
npm install
npm run dev  # starts Vite dev server, usually on http://localhost:5173
```

### 4) 
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
Performance Tests: Load testing with large files

## Docker

Run your project using docker
