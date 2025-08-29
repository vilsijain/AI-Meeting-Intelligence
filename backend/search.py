
from typing import List, Tuple, Optional
import chromadb
from chromadb.config import Settings

client = chromadb.PersistentClient(path="./backend/chroma_store", settings=Settings(allow_reset=True))
COLLECTION_NAME = "transcripts"
collection = client.get_or_create_collection(COLLECTION_NAME, metadata={"hnsw:space": "cosine"})

def add_chunks(meeting_id: int, chunks: List[str], embeddings: List[List[float]]):
    ids = [f"{meeting_id}:{i}" for i in range(len(chunks))]
    metadatas = [{"meeting_id": meeting_id, "chunk_idx": i} for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids, metadatas=metadatas)

def query(q: str, n: int = 5, meeting_id: Optional[int] = None) -> List[Tuple[str, float, int]]:
    where = {"meeting_id": meeting_id} if meeting_id is not None else None
    res = collection.query(query_texts=[q], n_results=n, where=where)
    docs = res.get("documents", [[]])[0]
    dists = res.get("distances", [[]])[0]
    metas = res.get("metadatas", [[]])[0]
    out = []
    for doc, dist, meta in zip(docs, dists, metas):
        out.append((doc, dist, int(meta.get("meeting_id"))))
    return out
