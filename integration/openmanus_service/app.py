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
from dotenv import load_dotenv

# Ensure project paths are on sys.path so we can import OpenManus and its 'app' package
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))
# Many modules inside OpenManus use absolute imports like `from app.x import ...`
# so we must also add the openmanus package directory itself to sys.path
OPENMANUS_DIR = PROJECT_ROOT / "openmanus"
if str(OPENMANUS_DIR) not in sys.path:
    sys.path.append(str(OPENMANUS_DIR))

# Load environment variables from .env files (project root and service dir)
try:
    load_dotenv(dotenv_path=PROJECT_ROOT / ".env", override=False)
    load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env", override=False)
except Exception:
    # Don't crash if dotenv isn't present; env vars can still come from the host
    pass

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
    "http://127.0.0.1:3001",
    "http://localhost:3001",
    "http://127.0.0.1:3002",
    "http://localhost:3002",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------- Request Logging -----------------------
import time as _time
from starlette.middleware.base import BaseHTTPMiddleware


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):  # type: ignore[override]
        _t0 = _time.time()
        try:
            path = request.url.path
        except Exception:
            path = "<unknown>"
        # ASCII-only to avoid Unicode issues on some terminals
        print(f"[REQUEST] {request.method} {path}")
        response = await call_next(request)
        dur_ms = (_time.time() - _t0) * 1000
        print(f"[RESPONSE] {request.method} {path} - {response.status_code} ({dur_ms:.2f}ms)")
        return response


app.add_middleware(LoggingMiddleware)


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
        "openmanus_error": str(_import_error) if _import_error else None,
        "luna_import": _luna_import_error is None,
        "luna_error": str(_luna_import_error) if _luna_import_error else None,
        "python_executable": sys.executable,
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


@app.get("/luna/reports/deep-scan")
async def luna_reports_deep_scan(niche: str) -> Dict[str, Any]:
    """Comprehensive premium niche intelligence report using DeepScanOrchestrator."""
    logger.info("/luna/reports/deep-scan called niche=%s", niche)
    try:
        from integration.research_tools.deep_scan_orchestrator import DeepScanOrchestrator
    except Exception as e:
        logger.exception("Failed to import DeepScanOrchestrator: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    import time as _time
    _start = _time.time()
    try:
        orch = DeepScanOrchestrator()
        report = await orch.generate_report(niche)
        _dur = _time.time() - _start
        logger.info("/luna/reports/deep-scan completed: %d items in %.2fs", len(report.get("items", [])), _dur)
        report["duration_seconds"] = round(_dur, 2)
        return {"success": True, **report}
    except Exception as e:
        logger.exception("Error in /luna/reports/deep-scan: %s", e)
        raise HTTPException(status_code=500, detail=str(e))



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
    import time as _time
    _start = _time.time()
    try:
        gg = goal.to_dataclass()
        luna = _get_luna()
        growth_plan = await luna.process_growth_goal(gg)
        _dur = _time.time() - _start
        # Safely compute an insights count for logging
        insights_count = -1
        if isinstance(growth_plan, dict):
            rs = growth_plan.get("research_summary")
            if isinstance(rs, dict):
                insights_count = len(rs.get("insights", []))
            else:
                # If summary is a string, we don't have a structured insights list
                insights_count = -1
        logger.info("/luna/process-goal completed in %.2fs (insights=%s)", _dur, insights_count)
        return {"success": True, "growth_plan": growth_plan, "duration_seconds": round(_dur, 2)}
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


@app.get("/luna/research/deep-scan")
async def luna_research_deep_scan(niche: str) -> Dict[str, Any]:
    """ScrapeDo-only deep extraction scan for high-fidelity metrics per domain."""
    logger.info("/luna/research/deep-scan called niche=%s", niche)
    try:
        from integration.research_tools.scrapedo_tool import ScrapeDoResearchTool
    except Exception as e:
        logger.exception("Failed to import ScrapeDoResearchTool: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    import time as _time
    _start = _time.time()
    try:
        tool = ScrapeDoResearchTool()
        report = await tool.deep_extraction_scan(niche)
        _dur = _time.time() - _start
        logger.info("/luna/research/deep-scan completed with %d items in %.2fs", len(report.get("items", [])), _dur)
        report["duration_seconds"] = round(_dur, 2)
        return {"success": True, **report}
    except Exception as e:
        logger.exception("Error in /luna/research/deep-scan: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


class ComprehensiveResearchRequest(BaseModel):
    niche: str
    goal: str = ""
    research_types: List[str] | None = None


@app.get("/luna/research/full")
async def luna_research_full(niche: str, goal: str = "") -> Dict[str, Any]:
    """Run comprehensive multi-provider research and return raw + synthesized insights."""
    logger.info("/luna/research/full called niche=%s goal=%s", niche, goal)
    try:
        from integration.research_tools import LunaResearchOrchestrator
    except Exception as e:
        logger.exception("Failed to import orchestrator: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
    orchestrator = LunaResearchOrchestrator()
    import time as _time
    _start = _time.time()
    try:
        result = await orchestrator.conduct_comprehensive_research(niche=niche, goal=goal or "")
        _dur = _time.time() - _start
        logger.info("/luna/research/full completed: %d raw insights in %.2fs", len(result.get("raw_insights", [])), _dur)
        result["duration_seconds"] = round(_dur, 2)
        return {"success": True, **result}
    except Exception as e:
        logger.exception("Error in /luna/research/full: %s", e)
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
