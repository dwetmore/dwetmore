import os
import sqlite3
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "/data/notes.db")
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

app = FastAPI(title="Notes App")

# Serve /static/*
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class NoteIn(BaseModel):
    title: str
    body: str

class NoteOut(NoteIn):
    id: int

def db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT)"
    )
    return conn

@app.get("/")
def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    try:
        conn = db()
        conn.execute("SELECT 1")
        conn.close()
        return {"ready": True}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))

@app.get("/api/notes", response_model=List[NoteOut])
def list_notes():
    conn = db()
    rows = conn.execute("SELECT id, title, body FROM notes ORDER BY id DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/notes", response_model=NoteOut)
def create_note(note: NoteIn):
    conn = db()
    cur = conn.execute("INSERT INTO notes (title, body) VALUES (?, ?)", (note.title, note.body))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"id": new_id, **note.model_dump()}

@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int):
    conn = db()
    cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="not found")
    return {"deleted": note_id}
