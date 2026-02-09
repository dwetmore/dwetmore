"""FastAPI app exposing a minimal chat UI and Ollama-backed API."""

from __future__ import annotations

import logging
import os
from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

logger = logging.getLogger(__name__)

app = FastAPI()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    """Return a basic health check payload."""
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    """Serve a tiny HTML UI for ad-hoc chat prompts."""
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Chatbot</title>
  <style>
    body { font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 16px; }
    .card { border: 1px solid #ddd; border-radius: 10px; padding: 16px; margin: 12px 0; }
    textarea { width: 100%; min-height: 120px; padding: 10px; border: 1px solid #bbb; border-radius: 8px; font-size: 14px; }
    button { padding: 10px 14px; border: 0; border-radius: 8px; cursor: pointer; font-weight: 600; background:#111; color:#fff; }
    pre { white-space: pre-wrap; }
    .meta { color:#666; font-size:12px; }
  </style>
</head>
<body>
  <h1>Chat</h1>
  <p class="meta">FastAPI → Ollama</p>
  <div class="card">
    <textarea id="prompt" placeholder="Ask something..."></textarea>
    <div style="margin-top:10px; display:flex; gap:10px;">
      <button onclick="send()">Send</button>
    </div>
    <p class="meta" id="status"></p>
  </div>
  <div class="card">
    <pre id="out"></pre>
  </div>

<script>
async function send() {
  const prompt = document.getElementById("prompt").value.trim();
  const status = document.getElementById("status");
  const out = document.getElementById("out");
  status.textContent = "";
  out.textContent = "";
  if (!prompt) { status.textContent = "Prompt required."; return; }

  try {
    const r = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt })
    });
    const t = await r.text();
    if (!r.ok) throw new Error(`${r.status} ${r.statusText}: ${t}`);
    const j = JSON.parse(t);
    out.textContent = j.response ?? JSON.stringify(j, null, 2);
    status.textContent = "Done.";
  } catch (e) {
    status.textContent = String(e);
  }
}
</script>
</body>
</html>
"""


@app.post("/api/chat")
async def chat(payload: dict[str, Any]) -> dict[str, str]:
    """Forward a prompt to Ollama and return the response."""
    prompt = (payload.get("prompt") or "").strip()
    if not prompt:
        return {"error": "prompt is required"}

    req = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}

    async with httpx.AsyncClient(timeout=180.0) as client:
        try:
            response = await client.post(f"{OLLAMA_BASE_URL}/api/generate", json=req)
            response.raise_for_status()
        except httpx.HTTPError:
            logger.exception("Ollama request failed")
            raise
        data = response.json()

    return {"model": data.get("model"), "response": data.get("response", "")}
