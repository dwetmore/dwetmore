import os
import sqlite3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


def get_db_path() -> str:
    return os.environ.get("DB_PATH", "/data/notes.db")


def ensure_database() -> None:
    db_path = get_db_path()
    db_dir = os.path.dirname(db_path)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path())


class NoteCreate(BaseModel):
    title: str
    body: str


class NoteOut(NoteCreate):
    id: int
    created_at: str


@app.on_event("startup")
def startup() -> None:
    ensure_database()


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return {"status": "ready"}
    except sqlite3.Error:
        raise HTTPException(status_code=503, detail="Database not ready")


@app.get("/api/notes", response_model=list[NoteOut])
def list_notes() -> list[NoteOut]:
    with get_connection() as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            "SELECT id, title, body, created_at FROM notes ORDER BY id"
        ).fetchall()
    return [NoteOut(**dict(row)) for row in rows]


@app.post("/api/notes", response_model=NoteOut, status_code=201)
def create_note(note: NoteCreate) -> NoteOut:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO notes (title, body) VALUES (?, ?)",
            (note.title, note.body),
        )
        note_id = cursor.lastrowid
        row = conn.execute(
            "SELECT id, title, body, created_at FROM notes WHERE id = ?",
            (note_id,),
        ).fetchone()
        conn.commit()
    return NoteOut(**dict(row))


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int) -> dict:
    with get_connection() as conn:
        cursor = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"status": "deleted"}
