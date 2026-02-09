import importlib
import sys
from pathlib import Path

import httpx
from fastapi.testclient import TestClient


def _load_app():
    app_dir = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(app_dir))
    import main  # noqa: PLC0415

    return importlib.reload(main)


def test_healthz():
    module = _load_app()
    client = TestClient(module.app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_prompt_required():
    module = _load_app()
    client = TestClient(module.app)
    response = client.post("/api/chat", json={"prompt": ""})
    assert response.status_code == 200
    assert response.json() == {"error": "prompt is required"}


def test_chat_success(monkeypatch):
    module = _load_app()

    response = httpx.Response(
        200,
        json={"model": "llama3.2", "response": "Hello"},
        request=httpx.Request("POST", "http://ollama:11434/api/generate"),
    )

    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            self.post_calls = []

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return None

        async def post(self, url, json):
            self.post_calls.append((url, json))
            return response

    monkeypatch.setattr(module.httpx, "AsyncClient", MockAsyncClient)

    client = TestClient(module.app)
    result = client.post("/api/chat", json={"prompt": "Hello"})

    assert result.status_code == 200
    assert result.json() == {"model": "llama3.2", "response": "Hello"}
