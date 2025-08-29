
import os, json
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
from .db import init_db, get_session
from . import crud
from .transcription import transcribe
from .extract import run_pipeline
from .schemas import InsightPayload, SearchHit
from .search import query as search_query

MEDIA_DIR = Path(__file__).parent / "media"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

app = FastAPI(title="AI Meeting Intelligence API", version="0.1.0")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

@app.post("/api/upload")
async def upload_meeting(file: UploadFile = File(...), session: Session = Depends(get_session)):
    # save file
    ext = Path(file.filename).suffix
    if ext.lower() not in [".mp3", ".wav", ".m4a", ".mp4", ".mov", ".mkv", ".webm"]:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    dst = MEDIA_DIR / file.filename
    content = await file.read()
    dst.write_bytes(content)

    # create meeting row
    meeting = crud.create_meeting(session, str(dst), title=file.filename)

    # transcribe
    transcript = transcribe(str(dst))

    # run pipeline (extract insights + add to vector db)
    insights = await run_pipeline(meeting.id, transcript)

    # persist insights as JSON strings
    ins = crud.create_insight(
        session,
        meeting_id=meeting.id,
        transcript=transcript,
        participants=json.dumps(insights.get("participants", [])),
        action_items=json.dumps(insights.get("action_items", [])),
        decisions=json.dumps(insights.get("decisions", [])),
    )

    return {"meeting_id": meeting.id, "insight_id": ins.id}

@app.get("/api/meetings")
def list_meetings(session: Session = Depends(get_session)):
    meetings = crud.get_meetings(session)
    return [
        {"id": m.id, "title": m.title, "created_at": m.created_at.isoformat()}
        for m in meetings
    ]

@app.get("/api/meetings/{meeting_id}")
def meeting_detail(meeting_id: int, session: Session = Depends(get_session)):
    m = crud.get_meeting_detail(session, meeting_id)
    if not m:
        raise HTTPException(status_code=404, detail="Meeting not found")
    ins = crud.get_insight_by_meeting(session, meeting_id)
    if not ins:
        raise HTTPException(status_code=404, detail="Insights not found")
    return {
        "id": m.id,
        "title": m.title,
        "created_at": m.created_at.isoformat(),
        "file_path": m.file_path,
        "transcript": ins.transcript,
        "participants": json.loads(ins.participants),
        "action_items": json.loads(ins.action_items),
        "decisions": json.loads(ins.decisions),
    }

@app.get("/api/search")
def search(q: str = Query(..., min_length=2), meeting_id: int | None = None):
    hits = search_query(q, n=5, meeting_id=meeting_id)
    return [
        {"text": t, "distance": float(d), "meeting_id": mid} for (t, d, mid) in hits
    ]

@app.post("/api/transcribe")
async def debug_transcribe(file: UploadFile = File(...)):
    # For debugging
    ext = Path(file.filename).suffix
    if ext.lower() not in [".mp3", ".wav", ".m4a", ".mp4", ".mov", ".mkv", ".webm"]:
        raise HTTPException(status_code=400, detail="Unsupported file type.")
    dst = MEDIA_DIR / file.filename
    content = await file.read()
    dst.write_bytes(content)
    txt = transcribe(str(dst))
    return {"transcript": txt}
