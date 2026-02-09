"""FastAPI service providing a minimal SQLite-backed notes API."""

from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from typing import Iterator

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
    """Payload for creating or updating a note."""

    title: str
    body: str


class NoteOut(NoteIn):
    """Note response with the database identifier."""

    id: int


@contextmanager
def db_connection() -> Iterator[sqlite3.Connection]:
    """Yield a ready-to-use SQLite connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, body TEXT)"
    )
    try:
        yield conn
    finally:
        conn.close()


@app.get("/")
def root() -> FileResponse:
    """Serve the single-page app entry point."""
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Return a basic health check payload."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz() -> dict[str, bool]:
    """Check database connectivity for readiness probes."""
    try:
        with db_connection() as conn:
            conn.execute("SELECT 1")
        return {"ready": True}
    except Exception as exc:  # pragma: no cover - defensive for unexpected DB failures
        raise HTTPException(status_code=503, detail=str(exc))


@app.get("/api/notes", response_model=list[NoteOut])
def list_notes() -> list[dict[str, str | int]]:
    """Return all notes ordered by most recent first."""
    with db_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, body FROM notes ORDER BY id DESC"
        ).fetchall()
    return [dict(r) for r in rows]


@app.post("/api/notes", response_model=NoteOut)
def create_note(note: NoteIn) -> dict[str, str | int]:
    """Persist a note and return the created record."""
    with db_connection() as conn:
        cur = conn.execute(
            "INSERT INTO notes (title, body) VALUES (?, ?)", (note.title, note.body)
        )
        conn.commit()
        new_id = cur.lastrowid
    return {"id": new_id, **note.model_dump()}


@app.delete("/api/notes/{note_id}")
def delete_note(note_id: int) -> dict[str, int]:
    """Delete a note by id."""
    with db_connection() as conn:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="not found")
    return {"deleted": note_id}
