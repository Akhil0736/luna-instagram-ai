from __future__ import annotations

import os
import sys
import logging
from dataclasses import asdict
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# ------------------------- Logging -------------------------
logger = logging.getLogger("openmanus_service")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))

# ------------------------- CORS ----------------------------
frontend_origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
allowed_origins = [
    frontend_origin,
    "http://127.0.0.1:3000",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

# ------------------------- Luna Agent ----------------------
try:
    from integration.luna_agent import LunaAgent
    from integration.models import GrowthGoal, ResearchInsight
except Exception as e:
    LunaAgent = None  # type: ignore
    GrowthGoal = None  # type: ignore
    ResearchInsight = None  # type: ignore
    _luna_import_error = e
else:
    _luna_import_error = None


class GrowthGoalModel(BaseModel):
    target_metric: str
    target_increase: float
    timeline_days: int
    niche: str
    current_followers: Optional[int] = None
    notes: Optional[str] = None

    def to_dataclass(self) -> "GrowthGoal":  # type: ignore[name-defined]
        if not GrowthGoal:
            raise RuntimeError(f"Luna models unavailable: {_luna_import_error}")
        return GrowthGoal(
            target_metric=self.target_metric,  # type: ignore[arg-type]
            target_increase=self.target_increase,
            timeline_days=self.timeline_days,
            niche=self.niche,
            current_followers=self.current_followers,
            notes=self.notes,
        )


@app.get("/health")
async def health() -> Dict[str, Any]:
    return {
        "ok": True,
        "openmanus_import": _import_error is None,
        "luna_import": _luna_import_error is None,
    }


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


# ========================= LUNA API =========================

def _get_luna() -> "LunaAgent":  # type: ignore[name-defined]
    if _luna_import_error:
        raise HTTPException(status_code=500, detail=f"Failed to import LunaAgent: {_luna_import_error}")
    # Basic singleton per-process
    global _LUNA_SINGLETON
    try:
        _LUNA_SINGLETON
    except NameError:
        _LUNA_SINGLETON = LunaAgent()  # type: ignore[operator]
    return _LUNA_SINGLETON  # type: ignore[return-value]


@app.post("/luna/process-goal")
async def luna_process_goal(goal: GrowthGoalModel) -> Dict[str, Any]:
    """Accept a GrowthGoal JSON and return a complete growth plan."""
    logger.info("/luna/process-goal called for niche=%s", goal.niche)
    try:
        gg = goal.to_dataclass()
        luna = _get_luna()
        growth_plan = await luna.process_growth_goal(gg)
        return {"success": True, "growth_plan": growth_plan}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /luna/process-goal: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/luna/research/{niche}")
async def luna_research(niche: str) -> Dict[str, Any]:
    """Quick research endpoint to test research layer for a niche."""
    logger.info("/luna/research called for niche=%s", niche)
    try:
        if not GrowthGoal:
            raise RuntimeError(f"Luna models unavailable: {_luna_import_error}")
        luna = _get_luna()
        dummy_goal = GrowthGoal(
            target_metric="followers",
            target_increase=0.2,
            timeline_days=30,
            niche=niche,
            current_followers=0,
        )
        insights = await luna.conduct_multi_source_research(dummy_goal)
        # Convert dataclass objects to dicts
        insights_json = [asdict(i) for i in insights]
        return {"success": True, "niche": niche, "insights": insights_json}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /luna/research: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


class ApprovePlanRequest(BaseModel):
    approved_plan: Dict[str, Any]


@app.post("/luna/approve-plan")
async def luna_approve_plan(req: ApprovePlanRequest) -> Dict[str, Any]:
    """Handle user approval and trigger execution via Riona (placeholder)."""
    logger.info("/luna/approve-plan called")
    try:
        luna = _get_luna()
        results = await luna.execute_approved_plan(req.approved_plan)
        return {"success": True, "execution_results": results}
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Error in /luna/approve-plan: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
