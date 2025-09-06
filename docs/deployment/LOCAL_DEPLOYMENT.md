# Luna 4-Service Local Deployment Guide

This guide helps you run the complete Luna stack locally with Docker Compose:

- Ollama — local AI model hosting for embeddings and local LLMs
- OpenManus — research, semantic analysis, strategy generation, and orchestration (FastAPI)
- Riona — Instagram automation engine (REST)
- Luna Frontend — Next.js user interface
- Redis — execution state tracking

## Prerequisites

- Docker and Docker Compose
- API token for Riona (set as `RIONA_API_TOKEN`)

## Services and Ports

- Ollama: http://localhost:11434
- OpenManus (backend): http://localhost:8000
- Riona: http://localhost:8080 (example)
- Frontend: http://localhost:3000
- Redis: redis://localhost:6379/0

## Environment

Create a `.env` file at the project root with sensitive variables:

```
RIONA_API_TOKEN=REPLACE_ME
APIFY_TOKEN=
SCRAPEDO_API_KEY=
TAVILY_API_KEY=
```

Backend example env: `integration/openmanus_service/.env.example`

Frontend example env: `frontend/.env.local.example`

## Bring up the stack

```
docker compose up -d --build
```

Seed the Ollama embedding model (first time only):

```
docker exec -it ollama ollama pull mxbai-embed-large
```

## Health checks

- Backend root: `GET http://localhost:8000/`
- Semantic: `POST http://localhost:8000/semantic/understand`
  - Body: `{ "text": "I want to grow from 0 to 5000 followers in 90 days, fitness coaching" }`
- Frontend: `http://localhost:3000`
- Riona: use your Riona health endpoint (varies by deployment)

## Configuration

OpenManus (backend) reads:

- `FRONTEND_ORIGIN=http://localhost:3000` (CORS)
- `EMBEDDINGS_BACKEND=ollama`
- `OLLAMA_HOST=http://ollama:11434`
- `OLLAMA_EMBED_MODEL=mxbai-embed-large`
- `RIONA_BASE_URL=http://riona:8080/api`
- `RIONA_API_TOKEN=<your-token>`
- `REDIS_URL=redis://redis:6379/0`

Frontend reads:

- `NEXT_PUBLIC_LUNA_API_BASE=http://localhost:8000`

## Workflow validation

1. From the frontend, enter a goal like:
   - "I want to grow from 0 to 5000 followers in 90 days, fitness coaching"
2. Frontend calls `POST /semantic/understand`, then `POST /luna/process-goal`.
3. (Priority 2) `POST /luna/execute-autonomous-growth` will create an execution, dispatch tasks to Riona via `LunaRionaBridge`, and return an `execution_id`.
4. Poll `GET /luna/execution-status/{id}` (and later `WS /ws/execution/{id}`) to watch progress in real-time.

## Troubleshooting

- If semantic endpoint returns 503, ensure Ollama is running and the embedding model is pulled.
- If Riona dispatch fails, confirm `RIONA_BASE_URL` and `RIONA_API_TOKEN` are set and Riona service is reachable.
- For local-only testing without Redis, the bridge will fall back to a file-backed state at `.state/riona_state.json`.

## Production next steps

- Reuse `docker-compose.yml` on a single VM (Oracle Free Tier 24GB RAM recommended).
- Add TLS with Traefik/Caddy/nginx.
- Use managed Redis or persistent Redis volume.
- Add CI/CD and observability (logs/metrics/alerts).
