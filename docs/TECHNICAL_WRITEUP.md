# Technical Write-up

## 1) Architecture Decisions
- **FastAPI + SQLModel (SQLite)** keeps the backend simple, strongly typed, and easy to introspect with built-in OpenAPI docs.
- **Local-first AI** via **Whisper.cpp** and **Ollama** reduces cloud complexity. Both are swappable if you later move to hosted services.
- **ChromaDB** provides lightweight, embedded vector search with persistence.
- **React + Tailwind** enables a fast, clean UI with minimal config; Vite for DX and speed.

## 2) AI Pipeline Implementation
1. **Upload** audio/video -> stored in `backend/media/` with a Meeting row created.
2. **Transcription** via Whisper.cpp (CLI). If unavailable, a stub transcript is produced for demo.
3. **Chunking + Embedding**: transcript is chunked (~1k chars) and embedded with Ollama-embeddings or a simple fallback (hash-based) for demo. Chunks are inserted into ChromaDB with `meeting_id` metadata.
4. **Info Extraction** via LLM (Ollama): a structured JSON schema is requested: `action_items`, `decisions`, `participants`. If Ollama is unavailable, a deterministic stub is returned.
5. **Search** uses ChromaDB similarity on stored chunks, optionally filtered by `meeting_id`.
6. **Persist** core entities in SQLite (Meeting, Insight, ActionItem, Decision, Participant).

## 3) Challenges and Solutions
- **Audio/Video diversity**: Whisper.cpp flags vary by format. We wrap subprocess calls and fall back gracefully.
- **LLM determinism**: For testing, set `temperature=0` and fixed prompts; include a stub path for CI.
- **Latency**: For assignment scope we process synchronously; in production a task queue (Celery/Redis) would be used.
- **Schema drift**: Use Pydantic/SQLModel schemas and versioned prompts.

## 4) Evaluation Criteria (How this repo addresses them)
- **Correctness**: Endpoints are typed and covered by simple stubs when AI is offline.
- **Completeness**: Upload, dashboard, insights, and search implemented minimally.
- **Code Organization**: Separate modules for db, crud, llm, transcription, extraction, search.
- **Docs**: README + this write-up.
- **Error Handling**: Try/except on external tools, HTTPException surfaces clear messages.
- **API Design**: RESTful `/api/*`, returns JSON with IDs and lists.

## 5) Code Quality & Organization
- Modules by concern; small functions with clear contracts.
- Explicit `schemas` for requests/responses; `models` for DB.
- Single source of truth for database in `db.py`.

## 6) API Design
- `POST /api/upload` -> `{ meeting_id }` and runs pipeline synchronously.
- `GET /api/meetings` -> list with basic metadata.
- `GET /api/meetings/{id}` -> full detail, incl. insights.
- `GET /api/search?q=...&meeting_id=` -> semantic search via ChromaDB.
- `POST /api/transcribe` (internal/debug) -> returns transcript text.
- Auto docs at `/docs`.

## 7) AI/ML Pipeline
- Prompt template requests strict JSON. Parsed with safe loader; validated against Pydantic models.
- Embeddings: attempt Ollama `/api/embeddings`; fallback to hashed vectors for demo stability.
- Vector DB: Chroma persistent store per repo, one collection (`transcripts`).

## 8) Error Handling
- External calls wrapped; on failure, return `503` with hint to enable services.
- Input validation for upload mime/size (basic).
- Centralized exception handlers can be added as future work.

## 9) Documentation
- Inline docstrings on public functions.
- README covers setup and commands.
- This write-up explains reasoning and tradeoffs.
