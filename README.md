# notes-app

Minimal FastAPI notes service with SQLite storage, built for local WSL use and MicroK8s deployment.

## Repo layout

```
/app
  main.py
  requirements.txt
  Dockerfile
/deploy
  notes.yaml
```

## Local run (WSL)

```bash
cd /workspace/dwetmore/app
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DB_PATH=./notes.db uvicorn main:app --host 0.0.0.0 --port 8000
```

Test:

```bash
curl http://localhost:8000/healthz
curl -X POST http://localhost:8000/api/notes \
  -H 'content-type: application/json' \
  -d '{"title":"t","body":"b"}'
curl http://localhost:8000/api/notes
```

## Build with Podman

```bash
cd /workspace/dwetmore/app
podman build -t notes-app:0.1 .
```

## Push to MicroK8s registry (localhost:32000)

```bash
podman tag notes-app:0.1 localhost:32000/notes-app:0.1
podman push localhost:32000/notes-app:0.1
```

## Deploy to MicroK8s

```bash
microk8s enable dns ingress storage registry
microk8s kubectl apply -f /workspace/dwetmore/deploy/notes.yaml
microk8s kubectl -n notes get pods,svc,ingress
```

## Verify via Ingress

```bash
curl -H "Host: notes.local" http://localhost/healthz
curl -H "Host: notes.local" http://localhost/api/notes
```
