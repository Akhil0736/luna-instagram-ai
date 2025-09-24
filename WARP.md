# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

Project scope
- Stack: FastAPI backend (OpenManus service), optional Riona automation service, Redis, and Ollama for embeddings. Node-based test utilities are included. Shared code exists for Python and TypeScript.
- Primary backend lives at integration/openmanus_service (FastAPI). Full local stack is orchestrated via docker-compose.yml.
- Deployment guide: docs/deployment/LOCAL_DEPLOYMENT.md.

Common commands
- Backend (OpenManus service)
  - Install (service-only): pip install -r integration/openmanus_service/requirements.txt
  - Run locally (reload, dev): from integration/openmanus_service, run uvicorn app:app --reload --host 0.0.0.0 --port 8091
  - Health check (local uvicorn): curl http://localhost:8091/health
  - Health check (docker compose): curl http://localhost:8000/health
- Full stack via Docker Compose
  - Start/build: docker compose up -d --build
  - Seed Ollama embeddings model (first-time): docker exec -it ollama ollama pull mxbai-embed-large
  - Default endpoints:
    - Ollama: http://localhost:11434
    - OpenManus: http://localhost:8000
    - Riona (example): http://localhost:8080
    - Redis: redis://localhost:6379/0
- Python tests (pytest)
  - Run all: pytest -c tests/python/pytest.ini
  - Single file: pytest -c tests/python/pytest.ini tests/python/test_sanity.py -q
  - Single test: pytest -c tests/python/pytest.ini tests/python/test_sanity.py::test_truth -q
  - Exclude integration tests: pytest -c tests/python/pytest.ini -m "not integration"
- JavaScript/TypeScript tests (Jest)
  - Run all: npx jest -c tests/js/jest.config.js
  - Single file: npx jest -c tests/js/jest.config.js tests/js/__tests__/sanity.test.ts
  - Single test name: npx jest -c tests/js/jest.config.js -t "true is truthy"
- Service smoke checks (Node scripts)
  - Check OpenManus/Riona health:
    - OPENMANUS_URL=http://localhost:8091 RIONA_URL=http://localhost:3001/api node tests/scripts/check_services.js
  - E2E (requires IG session cookie):
    - IG_SESSION_ID={{IG_SESSION_ID}} RIONA_URL=http://localhost:3001/api node tests/scripts/e2e_actions.js
- Lint
  - No repo-level linter config was found for Python or TypeScript.

Environment and configuration
- Core environment variables (used by code or docker-compose):
  - OPENROUTER_API_KEY, PARALLEL_AI_API_KEY
  - FRONTEND_ORIGIN (CORS), EMBEDDINGS_BACKEND=ollama, OLLAMA_HOST=http://ollama:11434, OLLAMA_EMBED_MODEL=mxbai-embed-large
  - RIONA_BASE_URL, RIONA_API_TOKEN
  - REDIS_URL
  - Optional research providers: APIFY_TOKEN, SCRAPEDO_API_KEY, TAVILY_API_KEY
- .env usage:
  - The service loads env from /root/luna-instagram-ai/.env when running in-container. For local dev, export variables in your shell.
- Ports:
  - Local uvicorn (dev): 8091
  - Docker Compose (OpenManus): 8000

High-level architecture
- FastAPI service (OpenManus)
  - Entry: integration/openmanus_service/app.py
    - Core endpoints:
      - Consultation: POST /luna/consultation/start, GET /luna/consultation/status/{user_id}, GET /luna/system/info
      - Riona integration (execution and status): routes under /luna/riona and /luna/execution
      - Health checks: /health and /
    - LLM clients: utils/llm_clients/openrouter_client.py (routes tasks to OpenRouter models by task category)
  - Orchestration (multi-agent)
    - orchestration/luna_master_orchestrator.py coordinates end-to-end flows:
      - ConversationAgent: context extraction and follow-up questions
      - ResearchAgent: parallel research with graceful stubs/fallbacks when API keys are missing
      - StrategyAgent: specialist “agents” (content, engagement, funnel, growth) debate/synthesize a comprehensive strategy
      - ExecutionAgent: implementation plan (timeline, content calendar, automation scope, resource estimates)
    - Maintains per-user conversation state (stage, context, research, final strategy)
- Research orchestration layer
  - integration/research_tools/orchestrator.py runs multiple providers (Tavily, ScrapeDo, Apify) concurrently, synthesizes results, and falls back to simpler providers if needed.
  - integration/models.py defines normalized models (e.g., ResearchInsight).
  - Optional semantic re-ranking via integration/openmanus_service/semantic (when Ollama embeddings are available).
- Riona integration (automation control plane)
  - integration/openmanus_service/integration/riona_controller:
    - StrategyExecutionPlanner converts strategy + execution_plan to concrete tasks (likes, follows, comments, hashtag research, audience research, analytics).
    - RionaTaskFilter enforces strict safety boundaries (excludes posting/DMs; allows engagement, research, analytics).
    - RionaController queues and simulates async execution; EnhancedRionaController adds per-user executors with rate-limited, humanized actions (placeholders for actual API calls).
- Shared code
  - shared/ contains cross-language utilities and types:
    - Python: shared/utils/python, shared/types/python
    - TypeScript: shared/utils/typescript, shared/types/typescript
  - Jest config maps @shared/* to shared/* for tests.

Production deployment
- Requirements
  - Docker and Docker Compose
  - OpenRouter API key (required)
  - Parallel AI API key (required for research features)
  - Redis instance (or memory fallback)
  - Ollama with mxbai-embed-large model
- Scaling considerations
  - Horizontal scaling via load balancer
  - Redis cluster for distributed caching
  - Ollama clustering for embeddings
  - Rate limit management for both OpenRouter and Parallel AI
  - Research task queuing for high-volume scenarios
- Security
  - API key validation for all external services
  - Rate limiting per service
  - Input sanitization and validation
  - Error message sanitization
  - Secure environment variable management

Cost optimization features
- Intelligent service selection
  - OpenRouter for fast, cost-effective generation
  - Parallel AI only for research-intensive queries
  - Local Ollama for embeddings (free after setup)
  - Smart caching for both generation and research results
- Research cost management
  - Longer cache TTL for research results (10–30 minutes)
  - Query deduplication for similar research requests
  - Fallback simulation mode for development
  - Usage analytics and cost tracking

This architecture provides a production-ready, cost-optimized AI system for Instagram growth coaching with world-class research capabilities powered by the synergy between OpenRouter's diverse LLM access and Parallel AI's enterprise-grade research intelligence.

Notes and caveats
- Health response shape vs tests: Current /health returns status/timestamp/integration flags. Some tests expect body.ok == True; adjust tests or unify the health response if you encounter failures.
- Ports: Local uvicorn uses 8091; docker-compose maps service on 8000.
- Riona service path: docker-compose references integration/riona (not present here). To exercise Riona-dependent flows locally, point to an existing Riona instance (set RIONA_URL / RIONA_BASE_URL) or remove that service from compose.
- Linting: No repo-level Python/TypeScript lint configuration was found.

Key docs
- docs/deployment/LOCAL_DEPLOYMENT.md (end-to-end local stack, env vars, model seeding, workflow validation, troubleshooting)
- integration/openmanus_service/README.md (service-level run instructions and endpoints)
- tests/README.md (test layout and quickstart for Python and JS)
