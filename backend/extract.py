
from typing import List
from .llm import generate_structured_insights, embed_texts
from .search import add_chunks

def chunk_text(text: str, max_len: int = 1000, overlap: int = 100) -> List[str]:
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+max_len]
        chunks.append(chunk)
        i += max_len - overlap
    return chunks

async def run_pipeline(meeting_id: int, transcript: str):
    # Extract insights
    insights = await generate_structured_insights(transcript)

    # Vectorize transcript chunks
    chunks = chunk_text(transcript)
    embeddings = await embed_texts(chunks)
    add_chunks(meeting_id, chunks, embeddings)

    return insights
