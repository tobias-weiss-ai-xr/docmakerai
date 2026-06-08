# DocMaker AI

**Automated AI-powered tutorial & documentation generation for end-user software.**

DocMaker AI is a pluggable pipeline that automatically creates step-by-step tutorials, user guides, and interactive walkthroughs from any web-based application — starting with **SOGo Groupware**. It uses Playwright to explore the UI, LLMs to understand and describe each step, and static-site generators to publish polished documentation with an embedded RAG chatbot.

---

## Architecture

```
User Interface (SOGo / any web app)
         │
         ▼
┌──────────────────────────────────────────────┐
│  1. CAPTURE  (Playwright MCP)                 │
│  • Auto-navigate SOGo workflows               │
│  • Screenshot every interaction               │
│  • Inject CSS highlights on clicked elements   │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  2. GENERATE  (aidocs-cli / SourceScribe)     │
│  • LLM analyzes screenshots + DOM context     │
│  • Generates step-by-step markdown tutorials  │
│  • Creates Mermaid diagrams for workflows     │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  3. PUBLISH  (Docusaurus + Shepherd.js)       │
│  • Static site with full-text search          │
│  • Versioned documentation                    │
│  • Interactive in-app tours via Shepherd.js   │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  4. RAG LAYER  (docs.ai / Ask0)              │
│  • Users ask "how do I share a calendar?"     │
│  • Semantic search across all tutorials       │
│  • LLM answers with source citations          │
└──────────────────────────────────────────────┘
```

### Core Principles

- **100% open source** — no proprietary lock-in, self-host everything
- **Local-first development** — run the full pipeline on a laptop
- **LLM-agnostic** — swap between OpenAI, Anthropic, Ollama (local), or any OpenAI-compatible API
- **App-agnostic** — works with any web application, not just SOGo
- **Incremental** — regenerate only changed tutorials via git-aware diffing

---

## Project Structure

```
docmakerai/
├── docs/                         # Generated documentation output
├── tutorials/                    # Raw tutorial markdown sources
│   └── sogo/                     # SOGo-specific tutorials
├── capture/                      # Playwright capture scripts
│   ├── playwright-mcp.json       # MCP server config
│   └── workflows/                # Workflow definitions (YAML)
├── generator/                    # Tutorial generation logic
│   ├── templates/                # Doc templates
│   └── config/                   # LLM provider config
├── site/                         # Docusaurus site source
│   ├── docusaurus.config.ts
│   └── src/
│       └── components/
│           └── ShepherdTour/     # Interactive tour components
├── rag/                          # RAG service
│   ├── api/                      # FastAPI backend
│   └── embedder/                 # Embedding pipeline
├── docker-compose.yml            # Production deployment
├── Dockerfile                    # Multi-stage build
├── .github/                      # CI/CD workflows
│   └── workflows/
│       └── deploy.yml            # Auto-deploy to contextual-intelligence.org
├── LICENSE
└── README.md
```

---

## Local Development

### Prerequisites

- Node.js 20+
- Python 3.12+
- Docker & Docker Compose (for production parity)
- An LLM API key (OpenAI / Anthropic) or Ollama (local)

### Quick Start

```bash
# 1. Clone & install
git clone https://github.com/your-org/docmakerai.git
cd docmakerai
npm install

# 2. Configure
cp .env.example .env
# Edit .env with your LLM API key

# 3. Capture a SOGo workflow
npx @playwright/mcp &
node capture/workflows/sogo-calendar-new-event.js

# 4. Generate tutorials
npx aidocs-cli generate

# 5. Preview docs locally
npm run docs:dev
# → http://localhost:3000

# 6. Test RAG
cd rag && pip install -r requirements.txt && uvicorn api.main:app --reload
```

### Environment Variables

| Variable | Description | Default |
|---|---|---|
| `LLM_PROVIDER` | `openai`, `anthropic`, or `ollama` | `ollama` |
| `LLM_API_KEY` | API key for the LLM provider | — |
| `LLM_MODEL` | Model name | `gpt-4o-mini` |
| `SOGO_URL` | SOGo instance URL | `http://localhost:8080` |
| `OUTPUT_DIR` | Generated docs output | `./docs` |
| `RAG_DB_PATH` | Vector database path | `./data/vectordb` |

---

## Roadmap

### Epic 1: Core Pipeline (Sprints 1–3)

**Goal**: End-to-end tutorial generation for SOGo from a single command.

#### Sprint 1 — Capture Foundation _(Current)_

| User Story | Status |
|---|---|
| As a developer, I can run Playwright MCP against a SOGo instance and navigate login + mail views | 🚧 In progress |
| As a developer, I can capture screenshots at each step with CSS highlights on interacted elements | ⬜ Not started |
| As a developer, I can define workflows as declarative YAML files (login → compose → send) | ⬜ Not started |
| As a developer, I can replay a captured workflow headlessly in CI | ⬜ Not started |

**Deliverables**: `capture/` directory with Playwright scripts + YAML workflow definitions for 3 core SOGo flows (login, read mail, compose mail).

#### Sprint 2 — Generation Engine

| User Story | Status |
|---|---|
| As a developer, I can run `aidocs-cli generate` on captured screenshots and get markdown tutorials | ⬜ Not started |
| As a developer, I can configure which LLM provider to use via environment variable | ⬜ Not started |
| As a developer, I can preview generated tutorials in my browser | ⬜ Not started |
| As a developer, generated tutorials include Mermaid workflow diagrams | ⬜ Not started |
| As a developer, I can customize tutorial templates per application | ⬜ Not started |

**Deliverables**: Generator configuration, template system, working `generate` command producing 3+ SOGo tutorials.

#### Sprint 3 — Documentation Site

| User Story | Status |
|---|---|
| As a user, I can browse all SOGo tutorials organized by topic (Mail, Calendar, Contacts, Admin) | ⬜ Not started |
| As a user, I can search across all tutorials with full-text search | ⬜ Not started |
| As a user, tutorials include numbered steps with annotated screenshots | ⬜ Not started |
| As a developer, I can version documentation and publish new versions | ⬜ Not started |

**Deliverables**: Docusaurus site deployed locally, all SOGo tutorials published, search working.

---

### Epic 2: Interactive Experience (Sprints 4–5)

**Goal**: Users can ask questions and get guided tours.

#### Sprint 4 — RAG Q&A

| User Story | Status |
|---|---|
| As a user, I can ask "How do I share a calendar?" and get an answer with a citation link to the relevant tutorial | ⬜ Not started |
| As a user, I can ask follow-up questions that remember context | ⬜ Not started |
| As a developer, the RAG pipeline indexes all tutorials automatically on generation | ⬜ Not started |
| As a developer, I can run the RAG service locally without external API calls (Ollama) | ⬜ Not started |

**Deliverables**: Working RAG chatbot embedded in the Docusaurus site, answering questions from generated SOGo tutorials.

#### Sprint 5 — Interactive In-App Tours

| User Story | Status |
|---|---|
| As a user, I can click "Take a tour" in the docs and see a step-by-step overlay on the SOGo interface | ⬜ Not started |
| As a user, the tour highlights the actual UI element I need to interact with | ⬜ Not started |
| As a user, I can navigate tours at my own pace (next/back/exit) | ⬜ Not started |
| As a developer, I can generate Shepherd.js tour definitions from the same workflow YAML files | ⬜ Not started |

**Deliverables**: Shepherd.js tour definitions auto-generated from capture workflows, embedded into the docs site.

---

### Epic 3: Production Deployment (Sprint 6)

**Goal**: Deploy to `docs.contextual-intelligence.org` for `chemie-lernen.org` users.

#### Sprint 6 — Docker Compose + Deployment

| User Story | Status |
|---|---|
| As a user, I can access SOGo tutorials at `docs.contextual-intellectual.org` | ⬜ Not started |
| As a developer, I can deploy the full stack (Docusaurus + RAG API) with a single `docker compose up` | ⬜ Not started |
| As a developer, tutorial regeneration runs automatically via GitHub Actions on push | ⬜ Not started |
| As a developer, I can roll back to a previous documentation version | ⬜ Not started |
| As an admin, I can monitor usage metrics (search queries, most-viewed tutorials) | ⬜ Not started |

**Deliverables**: Docker Compose configuration, CI/CD pipeline, deployment to `docs.contextual-intelligence.org`.

---

### Epic 4: Expand Coverage (Sprints 7–8)

**Goal**: Full SOGo coverage + support for additional applications.

#### Sprint 7 — SOGo Power User Flows

| User Story | Status |
|---|---|
| As a SOGo user, I can learn how to set up delegation (calendar/mail) | ⬜ Not started |
| As a SOGo user, I can learn how to configure server-side mail filters | ⬜ Not started |
| As a SOGo user, I can learn how to set up two-factor authentication | ⬜ Not started |
| As a SOGo user, I can learn how to use ActiveSync on my mobile device | ⬜ Not started |
| As a SOGo user, I can learn how to share address books with specific permissions | ⬜ Not started |

**Deliverables**: 15+ SOGo tutorials covering all major features.

#### Sprint 8 — Multi-App Support

| User Story | Status |
|---|---|
| As a developer, I can point DocMaker at any web application, not just SOGo | ⬜ Not started |
| As a developer, the RAG can ingest multiple application docs and disambiguate answers | ⬜ Not started |
| As a developer, each application has its own documentation namespace/section | ⬜ Not started |

**Deliverables**: Architecture abstracted for n-app support, documentation for onboarding new apps.

---

## Deployment

### Production Architecture

```
                          ┌─────────────────────────┐
                          │  Cloudflare (DNS + CDN)  │
                          │  docs.contextual-        │
                          │  intelligence.org        │
                          └──────────┬──────────────┘
                                     │
                          ┌──────────▼──────────────┐
                          │  Docker Host              │
                          │  (chemie-lernen.org VPS) │
                          │                           │
                          │  ┌─────────────────────┐  │
                          │  │  Caddy (TLS proxy)   │  │
                          │  └──────────┬──────────┘  │
                          │             │             │
                          │  ┌──────────▼──────────┐  │
                          │  │  Docusaurus (static) │  │
                          │  └─────────────────────┘  │
                          │  ┌─────────────────────┐  │
                          │  │  RAG API (FastAPI)   │  │
                          │  │  + ChromaDB          │  │
                          │  └─────────────────────┘  │
                          └───────────────────────────┘
```

### Docker Compose (planned)

```yaml
# docker-compose.yml (future)
services:
  docs:
    build:
      context: ./site
      dockerfile: ../Dockerfile
    ports:
      - "3000:3000"
    environment:
      - RAG_API_URL=http://rag-api:8000
    depends_on:
      - rag-api

  rag-api:
    build:
      context: ./rag
    ports:
      - "8000:8000"
    environment:
      - VECTOR_DB_PATH=/data/vectordb
    volumes:
      - vector-data:/data/vectordb

  rag-embedder:
    build:
      context: ./rag
    command: embedder --watch ./docs
    volumes:
      - ./docs:/docs:ro
      - vector-data:/data/vectordb

volumes:
  vector-data:
```

### CI/CD (planned)

```yaml
# .github/workflows/deploy.yml (future)
name: Deploy Docs
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate tutorials
        run: npx aidocs-cli generate
      - name: Build docs site
        run: npm run docs:build
      - name: Deploy to server
        run: |
          rsync -avz --delete site/build/ deploy@chemie-lernen.org:/var/www/docs/
          ssh deploy@chemie-lernen.org "docker compose up -d --build"
```

---

## License

MIT
