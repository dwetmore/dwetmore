import importlib
import os
import sys
from pathlib import Path

from fastapi.testclient import TestClient


def _load_app(db_path):
    app_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(app_dir))
    os.environ["DB_PATH"] = str(db_path)
    import main  # noqa: PLC0415

    return importlib.reload(main)


def test_healthz(tmp_path):
    module = _load_app(tmp_path / "notes.db")
    client = TestClient(module.app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_readyz(tmp_path):
    module = _load_app(tmp_path / "notes.db")
    client = TestClient(module.app)
    response = client.get("/readyz")
    assert response.status_code == 200
    assert response.json() == {"ready": True}


def test_create_and_list_notes(tmp_path):
    module = _load_app(tmp_path / "notes.db")
    client = TestClient(module.app)

    create = client.post("/api/notes", json={"title": "A", "body": "B"})
    assert create.status_code == 200
    assert create.json()["title"] == "A"

    listing = client.get("/api/notes")
    assert listing.status_code == 200
    assert listing.json()[0]["body"] == "B"


def test_delete_missing_note(tmp_path):
    module = _load_app(tmp_path / "notes.db")
    client = TestClient(module.app)

    response = client.delete("/api/notes/999")
    assert response.status_code == 404
