from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Ensure project root is on sys.path so we can import `openmanus`
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

try:
    # OpenManus LLM wrapper
    from openmanus.app.llm import LLM
except Exception as e:  # pragma: no cover - defensive import
    LLM = None  # type: ignore
    _import_error = e
else:
    _import_error = None

app = FastAPI(title="OpenManus Service", version="0.1.0")


class PlanRequest(BaseModel):
    goals: List[str] = Field(default_factory=list)
    niche: Optional[str] = None
    constraints: List[str] = Field(default_factory=list)
    # Optional: extra context
    audience: Optional[str] = None


class GenerateRequest(BaseModel):
    topic: str
    tone: Optional[str] = None
    length: Optional[str] = None
    format: Optional[str] = Field(
        default="caption",
        description="e.g., caption, dm, post_ideas, hashtag_list",
    )


class LLMService:
    _client: Optional[LLM] = None

    @classmethod
    def get_client(cls) -> LLM:
        if _import_error:
            raise RuntimeError(f"Failed to import OpenManus LLM: {_import_error}")
        if cls._client is None:
            # LLM will read provider keys from environment / OpenManus config
            cls._client = LLM()
        return cls._client


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {"ok": True, "openmanus_import": _import_error is None}


@app.post("/plan")
async def plan(req: PlanRequest) -> Dict[str, Any]:
    client = LLMService.get_client()

    goals_str = "\n".join(f"- {g}" for g in (req.goals or []))
    constraints_str = "\n".join(f"- {c}" for c in (req.constraints or []))

    prompt = f"""
You are an expert Instagram growth strategist.
Create a pragmatic, step-by-step 2-week campaign plan.

Niche: {req.niche or 'general'}
Audience: {req.audience or 'IG users'}
Goals:\n{goals_str or '- Increase reach and engagement'}
Constraints:\n{constraints_str or '- Keep under community guidelines'}

Return JSON with keys: objectives, content_calendar, engagement_playbook, metrics.
""".strip()

    try:
        text = await client.ask(
            messages=[{"role": "user", "content": prompt}],
            system_msgs=[{"role": "system", "content": "You plan and structure growth campaigns."}],
            stream=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"plan": text}


@app.post("/generate")
async def generate(req: GenerateRequest) -> Dict[str, Any]:
    client = LLMService.get_client()

    prompt = f"""
You are an expert Instagram copywriter.
Write content in the requested format.

Format: {req.format or 'caption'}
Topic: {req.topic}
Tone: {req.tone or 'friendly'}
Length: {req.length or 'short'}

Return concise, high-signal output suitable for posting.
If hashtags are relevant, include a final line starting with 'Hashtags:' followed by 5-10 hashtags.
""".strip()

    try:
        text = await client.ask(
            messages=[{"role": "user", "content": prompt}],
            system_msgs=[{"role": "system", "content": "You generate short-form social content."}],
            stream=False,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"content": text, "format": req.format or "caption"}
