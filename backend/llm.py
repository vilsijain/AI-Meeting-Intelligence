
import os, json
import httpx
from typing import Dict

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

EXTRACTION_PROMPT = lambda transcript: f"""
You are an AI assistant that extracts structured meeting insights from a transcript.
Return strict JSON with keys: participants, action_items, decisions.
Schema:
{{
  "participants": [{{"name": str, "role": str|null, "spoke_time_sec": float|null}}],
  "action_items": [{{"owner": str|null, "description": str, "due_date": str|null, "priority": "low"|"medium"|"high"}}],
  "decisions": [{{"summary": str, "rationale": str|null}}]
}}

Transcript:
{transcript}
Only return JSON, no prose.
"""
async def generate_structured_insights(transcript: str) -> Dict:
    # Try Ollama
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            r = await client.post(f"{OLLAMA_HOST}/api/generate", json={
                "model": OLLAMA_MODEL,
                "prompt": EXTRACTION_PROMPT(transcript),
                "options": {"temperature": 0}
            })
            r.raise_for_status()
            # Ollama streams lines; if 'done': true present, payload in 'response'
            data = r.json()
            text = data.get("response", "")
            # Attempt to parse JSON block
            text = text.strip()
            # allow models to wrap JSON in code fences
            if text.startswith("```"):
                text = text.strip("`")
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text)
    except Exception:
        # Fallback stub
        return {
            "participants": [{"name": "Alex", "role": "PM", "spoke_time_sec": 320.0}],
            "action_items": [
                {"owner": "Priya", "description": "Share sprint plan draft", "due_date": "2025-09-02", "priority": "high"}
            ],
            "decisions": [{"summary": "Move launch to Oct 10", "rationale": "QA bandwidth"}],
        }

async def embed_texts(texts: list[str]) -> list[list[float]]:
    # Try Ollama embeddings; fallback to deterministic fake embeddings
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(f"{OLLAMA_HOST}/api/embeddings", json={
                "model": "nomic-embed-text",  # change if you have another embeddings model
                "input": texts
            })
            r.raise_for_status()
            data = r.json()
            embs = data.get("data", [])
            return [e.get("embedding", []) for e in embs]
    except Exception:
        # Simple hash-based fixed-length vector for demo
        import math, random
        random.seed(42)
        def pseudo_vec(t: str, dim=256):
            v = [0.0]*dim
            for i, ch in enumerate(t.encode("utf-8")):
                v[i % dim] += (ch % 13) / 13.0
            # L2 normalize
            norm = math.sqrt(sum(x*x for x in v)) or 1.0
            return [x/norm for x in v]
        return [pseudo_vec(t) for t in texts]
