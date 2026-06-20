# TECH_SPEC.md

---

## 1. Project Overview

**Name:** `memory-sleuth`  
**Type:** Axentx product – a memory‑optimization tool for developers.  
**Goal:** Detect, diagnose, and recommend fixes for memory‑related bugs (leaks, fragmentation, over‑allocation, etc.) in C/C++ and Rust codebases, providing actionable insights in a CI‑friendly format.

---

## 2. Architecture Overview

```
┌─────────────────────┐
│  Client IDE/CLI     │
│  (VSCode, CLion,    │
│   command line)     │
└─────────────┬───────┘
              │
              ▼
┌─────────────────────┐
│  Agent Service       │
│  (Python/Go)         │
│  - Orchestrates      │
│    analysis runs     │
│  - Exposes REST API  │
└───────┬──────────────┘
        │
        ▼
┌─────────────────────┐
│  Analysis Engine     │
│  (Rust + vLLM)       │
│  - Static analysis   │
│  - Dynamic profiling │
│  - ML‑based anomaly  │
│    detection         │
└───────┬──────────────┘
        │
        ▼
┌─────────────────────┐
│  Data Store          │
│  (PostgreSQL +      │
│   pgvector)         │
│  - Code snapshots   │
│  - Profiling data   │
│  - Recommendations │
└───────┬──────────────┘
        │
        ▼
┌─────────────────────┐
│  Reporting Layer     │
│  (React + Node.js)   │
│  - Web UI            │
│  - CI badge generator│
└─────────────────────┘
```

* **Client**: IDE extensions or CLI trigger analysis.  
* **Agent Service**: Handles requests, schedules jobs, stores results.  
* **Analysis Engine**: Core logic – static analysis via `clang-tidy`, dynamic profiling via `Valgrind`/`AddressSanitizer`, ML inference with `vLLM` (LLM fine‑tuned on memory‑bug corpora).  
* **Data Store**: Persistent storage of code, metrics, and recommendations; vector embeddings for similarity search.  
* **Reporting Layer**: Generates human‑readable reports, CI badges, and optional pull‑request comments.

---

## 3. Components & Responsibilities

| Component | Language | Key Libraries | Responsibilities |
|-----------|----------|----------------|------------------|
| **Client Extension** | TypeScript | VSCode API, Node.js | Detects project root, collects file list, triggers Agent API. |
| **Agent Service** | Go | `gin`, `gorm`, `pgx` | REST API, job queue (`go-queue`), orchestrator, health checks. |
| **Analysis Engine** | Rust | `clang-sys`, `valgrind`, `serde`, `tokio`, `vllm` | Static analysis, dynamic profiling, ML inference, result aggregation. |
| **Data Store** | PostgreSQL 15 | `pgvector` extension | Stores code snapshots, profiling metrics, embeddings, recommendations. |
| **Reporting Layer** | React + Node.js | `express`, `react`, `chart.js` | Web UI, CI badge generator, PR comment formatter. |

---

## 4. Data Model

```sql
-- Code Snapshot
CREATE TABLE code_snapshot (
    id UUID PRIMARY KEY,
    repo_url TEXT NOT NULL,
    commit_hash TEXT NOT NULL,
    snapshot_ts TIMESTAMPTZ NOT NULL,
    files JSONB NOT NULL   -- { "path": "src/main.cpp", "content": "..." }
);

-- Profiling Result
CREATE TABLE profiling_result (
    id UUID PRIMARY KEY,
    snapshot_id UUID REFERENCES code_snapshot(id),
    tool TEXT NOT NULL,          -- "valgrind", "asan", etc.
    metrics JSONB NOT NULL,      -- {"allocations": 1234, "leaks": 3, ...}
    run_ts TIMESTAMPTZ NOT NULL
);

-- Analysis Report
CREATE TABLE analysis_report (
    id UUID PRIMARY KEY,
    snapshot_id UUID REFERENCES code_snapshot(id),
    report_json JSONB NOT NULL,  -- structured findings
    summary TEXT,
    created_at TIMESTAMPTZ NOT NULL
);

-- Recommendation
CREATE TABLE recommendation (
    id UUID PRIMARY KEY,
    report_id UUID REFERENCES analysis_report(id),
    file_path TEXT NOT NULL,
    line INT NOT NULL,
    issue_type TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    severity TEXT NOT NULL
);

-- Embedding for similarity search
CREATE TABLE code_embedding (
    id UUID PRIMARY KEY,
    snapshot_id UUID REFERENCES code_snapshot(id),
    vector VECTOR(1536)   -- 1536 from OpenAI embedding model
);
```

*All tables use `UUID` for global uniqueness and support sharding across repos.*

---

## 5. Key APIs / Interfaces

### 5.1 Agent Service REST API

| Endpoint | Method | Request | Response | Description |
|----------|--------|---------|----------|-------------|
| `/api/v1/analyze` | POST | `{ "repo_url": "...", "commit_hash": "...", "files": ["src/main.cpp"] }` | `{ "job_id": "..."} ` | Initiates analysis. |
| `/api/v1/status/{job_id}` | GET | – | `{ "status": "queued|running|completed|failed", "progress": 42 }` | Job status. |
| `/api/v1/report/{job_id}` | GET | – | `{ "report_id": "...", "summary": "..."} ` | Retrieves final report. |
| `/api/v1/health` | GET | – | `{ "status": "ok" }` | Health check. |

### 5.2 Analysis Engine CLI

```bash
memory-sleuth analyze \
  --repo /path/to/repo \
  --commit <hash> \
  --files src/main.cpp src/utils.cpp \
  --output /tmp/report.json
```

*Used internally by Agent Service; can be invoked manually for debugging.*

### 5.3 Reporting Layer Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/report/{report_id}` | GET | Returns HTML/JSON report. |
| `/api/v1/badge/{report_id}` | GET | Returns SVG badge for CI status. |
| `/api/v1/pr-comment/{report_id}` | POST | Generates PR comment payload. |

---

## 6. Technology Stack

| Layer | Technology | Reason |
|-------|------------|--------|
| **Client** | VSCode Extension (TypeScript) | Widely used IDE. |
| **Agent Service** | Go (Gin, GORM) | Fast, low‑latency API. |
| **Analysis Engine** | Rust + vLLM | Performance for static/dynamic analysis; LLM inference for anomaly detection. |
| **Data Store** | PostgreSQL 15 + pgvector | Relational integrity + vector search. |
| **Reporting** | React + Node.js (Express) | Rich UI, badge generation. |
| **CI Integration** | GitHub Actions | Badge, PR comment automation. |
| **Containerization** | Docker, Docker Compose | Reproducible builds. |
| **Orchestration** | Kubernetes (optional) | Scaling Agent & Engine. |

---

## 7. Dependencies

| Component | Dependency | Version | Notes |
|-----------|------------|---------|-------|
| **Agent Service** | `gin` | `v1.9.0` | HTTP framework. |
| | `gorm` | `v1.25.0` | ORM for PostgreSQL. |
| | `pgx` | `v4.15.0` | PostgreSQL driver. |
| | `go-queue` | `v1.0.0` | Job queue. |
| **Analysis Engine** | `clang-sys` | `v0.30.0` | Static analysis. |
| | `valgrind` | `v3.19.0` | Dynamic profiling. |
| | `vllm` | `v0.3.0` | LLM inference. |
| | `serde`, `tokio` | `v1.0` | Async runtime. |
| **Reporting Layer** | `react` | `v18.2.0` | UI. |
| | `express` | `v4.18.2` | API server. |
| | `chart.js` | `v4.3.0` | Visualizations. |
| **Data Store** | PostgreSQL | `15.3` | Core DB. |
| | `pgvector` | `v0.5.0` | Vector extension. |
| **CI** | `github-actions` | – | Workflow templates. |

---

## 8. Deployment

### 8.1 Local Development

```bash
# Build all services
docker compose build

# Start services
docker compose up -d

# Run tests
docker compose exec agent-service go test ./...
docker compose exec analysis-engine cargo test
```

### 8.2 Production

1. **Infrastructure**  
   - Kubernetes cluster (EKS/GKE/Azure AKS).  
   - Persistent PostgreSQL with `pgvector`.  
   - Object storage (S3) for large profiling logs.

2. **Deployment Pipeline**  
   - GitHub Actions: `build-and-push.yml` pushes Docker images to registry.  
   - Helm chart (`charts/memory-sleuth/`) deploys Agent, Engine, Reporting services.  
   - Auto‑scaling for Agent based on job queue length.

3. **CI Integration**  
   - GitHub Action `memory-sleuth.yml` runs analysis on PRs, posts badge, and PR comment.  
   - Badge URL: `https://memory-sleuth.example.com/api/v1/badge/{report_id}`.

4. **Monitoring**  
   - Prometheus metrics from Agent (`/metrics`).  
   - Grafana dashboards for job throughput, latency.  
   - Alertmanager for failed analyses.

---

## 9. Security & Compliance

| Area | Measures |
|------|----------|
| **Authentication** | API keys for Agent Service; OAuth for CI integration. |
| **Data Privacy** | All code snapshots are stored encrypted at rest (`pgcrypto`). |
| **Compliance** | Supports GDPR: data retention policy (90 days) and deletion endpoint. |
| **Vulnerability Management** | Dependabot alerts, regular image scanning (Trivy). |

---

## 10. Roadmap (High‑Level)

| Milestone | Description | Target |
|-----------|-------------|--------|
| **M1** | Complete static analysis integration (clang-tidy). | Q3 2026 |
| **M2** | Add dynamic profiling (Valgrind + ASan). | Q4 2026 |
| **M3** | ML anomaly detection with vLLM. | Q1 2027 |
| **M4** | CI badge + PR comment automation. | Q2 2027 |
| **M5** | Enterprise features: multi‑repo analytics, role‑based access. | Q3 2027 |

---

## 11. Appendix

### 11.1 Sample Report JSON

```json
{
  "summary": "3 memory leaks detected",
  "issues": [
    {
      "file": "src/main.cpp",
      "line": 42,
      "type": "Leak",
      "severity": "High",
      "suggestion": "Add delete[] after allocation."
    },
    {
      "file": "src/utils.cpp",
      "line": 88,
      "type": "Fragmentation",
      "severity": "Medium",
      "suggestion": "Use pool allocator."
    }
  ]
}
```

### 11.2 CI Workflow Snippet

```yaml
name: Memory Sleuth

on: [pull_request]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run memory-sleuth
        uses: axentx/memory-sleuth-action@v1
        with:
          repo-token: ${{ secrets.GITHUB_TOKEN }}
```

---
