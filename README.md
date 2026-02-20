# David Wetmore — Projects and Current Work

I build practical, well-documented software that blends AI-enabled apps with reliable deployment workflows.

## Projects

- **[argocd-apps](https://github.com/dwetmore/argocd-apps)**: App-of-apps bootstrap and workload Applications for Argo CD (chatbot, notes-app, GPU observability, space-invaders, cmatrix).
- **[chatbot-gitops](https://github.com/dwetmore/chatbot-gitops)**: Standalone GitOps repo for chatbot stack on MicroK8s.
- **[chatbot](https://github.com/dwetmore/chatbot)**: FastAPI chatbot application source.
- **[cmatrix-web](https://github.com/dwetmore/cmatrix-web)**: Browser-based cmatrix image (Xvfb + x11vnc + noVNC).
- **[gpu-observability-gitops](https://github.com/dwetmore/gpu-observability-gitops)**: GitOps GPU monitoring stack (DCGM exporter + Prometheus + Grafana + Loki).
- **[notes-app](https://github.com/dwetmore/notes-app)**: FastAPI + PostgreSQL notes service with K8s manifests and tests.
- **[space-invaders](https://github.com/dwetmore/space-invaders)**: Pygame app plus Kubernetes deployment manifests.
- **[dwetmore](https://github.com/dwetmore/dwetmore)**: Portfolio/meta repo that references and mirrors selected project content.

## Current Work (as of February 20, 2026)

- **argocd-apps (`main`)**: latest commit `77ee9ae` updates cmatrix deployment to `localhost:32000/cmatrix:novnc2`.
- **gpu-observability-gitops (`main`)**: latest commit `f78ad0a` expands GPU dashboard and aligns panels to supported DCGM metrics.
- **notes-app (`codex/fix-database-selection-logic-and-logging`)**: DB selection/overlay improvements in progress with local staged changes.
- **chatbot-gitops (`main`)**: migration cleanup state (dev-ollama patch files currently deleted locally).
- **dwetmore (`main`)**: portfolio repo with chatbot and notes project mirrors.

## Focus Areas

- Kubernetes + GitOps (Argo CD, Kustomize, Helm)
- GPU observability (DCGM, Prometheus, Grafana)
- Python services (FastAPI)
- Developer-focused demo apps and deployable workloads

## Contact

- GitHub: https://github.com/dwetmore
