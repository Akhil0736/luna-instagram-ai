# OpenManus Service (FastAPI)

A thin HTTP wrapper around the OpenManus agent components to expose planning and content-generation capabilities.

## Endpoints

- GET `/health` — health check
- POST `/plan` — generate a campaign plan
- POST `/generate` — generate content (caption, DM copy, post ideas, etc.)

## Run locally

Prereqs: Python 3.10+

```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8091
```

Alternatively:

```bash
python main.py
```

## Environment

Set your LLM provider keys (e.g., OpenAI, Azure, Bedrock) as required by `openmanus` (see `openmanus/README.md`). The service relies on OpenManus configuration (e.g., `config.toml`) for provider selection and model choices.

## Request examples

- POST `/plan`
```json
{
  "goals": ["Grow followers to 10k", "Increase engagement by 20%"],
  "niche": "fitness coaches",
  "constraints": ["No giveaways", "Organic only"]
}
```

- POST `/generate`
```json
{
  "topic": "Benefits of morning workouts",
  "tone": "friendly",
  "length": "short"
}
```
