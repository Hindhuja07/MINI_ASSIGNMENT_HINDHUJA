from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from models import Note, NoteCreate, NoteOut
from database import init_db, get_session
from sqlmodel import select
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None

@app.on_event("startup")
def startup():
    init_db()
    global model
    model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str) -> List[float]:
    vec = model.encode(text, show_progress_bar=False)
    return vec.tolist()

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

@app.post("/notes", response_model=NoteOut)
def create_note(note_in: NoteCreate):
    if not note_in.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    text_for_embedding = note_in.title + "\n" + note_in.content
    embedding = embed_text(text_for_embedding)
    embedding_str = json.dumps(embedding)
    note = Note(title=note_in.title, content=note_in.content, embedding=embedding_str)
    with get_session() as session:
        session.add(note)
        session.commit()
        session.refresh(note)
        return NoteOut(id=note.id, title=note.title, content=note.content)

@app.get("/notes", response_model=List[NoteOut])
def list_notes():
    with get_session() as session:
        notes = session.exec(select(Note)).all()
        return [NoteOut(id=n.id, title=n.title, content=n.content) for n in notes]

class SearchRequest(BaseModel):
    query: str
    top_k: int = 5

class SearchResult(BaseModel):
    id: int
    title: str
    content: str
    score: float

@app.post("/search", response_model=List[SearchResult])
def search_notes(req: SearchRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    query_vec = np.array(embed_text(query))
    with get_session() as session:
        notes = session.exec(select(Note)).all()
        scored = []
        for n in notes:
            if not n.embedding:
                continue
            emb = np.array(json.loads(n.embedding))
            score = cosine_sim(query_vec, emb)
            scored.append((score, n))
        scored.sort(key=lambda x: x[0], reverse=True)
        results = []
        for score, n in scored[: req.top_k]:
            results.append(SearchResult(id=n.id, title=n.title, content=n.content, score=round(float(score), 4)))
        return results

@app.get("/health")
def health():
    return {"status": "ok"}
