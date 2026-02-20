# 👋 David Wetmore — Projects & Current Work

> 🚀 I build practical, well-documented software that blends AI-enabled apps with reliable deployment workflows.

---

## 🌟 Featured Projects

### 🧭 [argocd-apps](https://github.com/dwetmore/argocd-apps)
- **What it is:** An Argo CD app-of-apps control repo that bootstraps and manages multiple workloads from one declarative entrypoint.
- **What it does:** Defines child Argo CD Applications for services like chatbot, notes-app, GPU observability, space-invaders, and cmatrix; keeps cluster state converged to Git.
- **Why it matters:** Demonstrates platform-level GitOps orchestration and how to scale from single apps to a managed portfolio with consistent deployment patterns.

### 🤖 [chatbot-gitops](https://github.com/dwetmore/chatbot-gitops)
- **What it is:** A deployment-focused repository for running the chatbot stack on MicroK8s via Kubernetes manifests and overlays.
- **What it does:** Manages environment-specific configuration and rollout behavior for OpenWebUI + Ollama, enabling repeatable local cluster deployments.
- **Why it matters:** Separates delivery concerns from application code and shows production-style configuration discipline even in homelab/dev environments.

### 🧠 [chatbot](https://github.com/dwetmore/chatbot)
- **What it is:** A FastAPI-based chatbot backend project.
- **What it does:** Exposes API endpoints and service logic that can be deployed independently or integrated into larger conversational systems.
- **Why it matters:** Highlights API-first backend design and provides a clean Python service foundation that can evolve with model providers and product requirements.

### 🖥️ [cmatrix-web](https://github.com/dwetmore/cmatrix-web)
- **What it is:** A containerized browser-accessible cmatrix experience built with Xvfb, x11vnc, and noVNC.
- **What it does:** Runs a terminal graphical workload in Kubernetes and serves it over HTTP so users can access it from any browser without local X11 setup.
- **Why it matters:** Demonstrates practical remote GUI packaging, container runtime behavior, and service exposure patterns for non-traditional workloads.

### 📊 [gpu-observability-gitops](https://github.com/dwetmore/gpu-observability-gitops)
- **What it is:** A pure GitOps observability stack for NVIDIA GPU environments on MicroK8s.
- **What it does:** Deploys and configures DCGM exporter, Prometheus, Grafana, and logging components with custom dashboards and metric curation.
- **Why it matters:** Shows end-to-end GPU telemetry implementation and operational monitoring maturity, which is critical for AI/ML reliability and capacity planning.

### 📝 [notes-app](https://github.com/dwetmore/notes-app)
- **What it is:** A FastAPI + PostgreSQL notes service with Kubernetes deployment assets and tests.
- **What it does:** Implements CRUD APIs, health/readiness endpoints, environment-driven DB backend selection, and deployable manifests for GitOps workflows.
- **Why it matters:** Demonstrates full-stack service engineering fundamentals: app logic, persistence behavior, test coverage, and deployment readiness.

### 👾 [space-invaders](https://github.com/dwetmore/space-invaders)
- **What it is:** A Pygame game project adapted for containerized/Kubernetes execution.
- **What it does:** Provides an interactive game workload with deployment manifests and runtime tuning for consistent behavior across environments.
- **Why it matters:** Proves that interactive apps can be treated with the same delivery rigor as backend services, strengthening platform versatility.

### 📁 [dwetmore](https://github.com/dwetmore/dwetmore)
- **What it is:** The portfolio/meta repository that documents and links the project ecosystem.
- **What it does:** Serves as the primary index for projects, current engineering focus, and public-facing technical narrative.
- **Why it matters:** Creates a single source of truth for project discovery and communicates architectural intent across the portfolio.

---

## 🔧 Current Work (as of February 20, 2026)

- ✅ **argocd-apps (`main`)**: latest commit `77ee9ae` updates cmatrix deployment to `localhost:32000/cmatrix:novnc2`.
- ✅ **gpu-observability-gitops (`main`)**: latest commit `f78ad0a` expands GPU dashboard and aligns panels to supported DCGM metrics.
- 🛠️ **notes-app (`codex/fix-database-selection-logic-and-logging`)**: DB selection/overlay improvements in progress with local staged changes.
- 🧹 **chatbot-gitops (`main`)**: migration cleanup state (dev-ollama patch files currently deleted locally).
- 📌 **dwetmore (`main`)**: portfolio repo with chatbot and notes project mirrors.

## 🎯 Focus Areas

- ☸️ Kubernetes + GitOps (Argo CD, Kustomize, Helm)
- 📈 GPU observability (DCGM, Prometheus, Grafana)
- 🐍 Python services (FastAPI)
- 🧪 Developer-focused demo apps and deployable workloads

## 📫 Contact

- GitHub: https://github.com/dwetmore
