from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from openmanus.app.agent.manus import Manus

from integration.models import (
    GrowthGoal,
    ResearchInsight,
    ContentRecommendation,
    AutomationTask,
)
from integration.research_tools import (
    ResearchTool,
    TavilyResearchTool,
    EnhancedTavilyResearchTool,
    WebCrawlerTool,
    SynthesisTool,
    QueryOptimizer,
    LunaResearchOrchestrator,
)


class LunaAgent:
    """Core orchestrator that turns growth goals into a research-backed plan.

    Phases:
    - Research (parallel, multi-source)
    - Strategy synthesis (via OpenManus / Manus)
    - Concrete recommendations (content + automation)
    - Plan packaging for approval
    """

    def __init__(self,
                 research_tools: Optional[List[ResearchTool]] = None,
                 manus_agent: Optional[Manus] = None) -> None:
        self.manus_agent = manus_agent or Manus()
        # Register research tools; default to enhanced Tavily + web crawler
        self.research_tools: List[ResearchTool] = research_tools or [
            EnhancedTavilyResearchTool(),
            WebCrawlerTool(),
        ]
        # Placeholder for later: an authenticated Riona client instance
        self.riona_client = None
        # Query optimizer and synthesis engine
        self.query_optimizer = QueryOptimizer(max_queries=25)
        self.synthesis = SynthesisTool()
        # Modular orchestrator managing multiple providers and smart routing
        self.research_orchestrator = LunaResearchOrchestrator()

    # --------------------------- Public API ---------------------------

    async def process_growth_goal(self, goal: GrowthGoal) -> Dict[str, Any]:
        """Main orchestration method that handles user growth goals."""
        logger = logging.getLogger(__name__)
        t0 = time.time()
        # Phase 1: Multi-source research (prefer comprehensive orchestrator)
        try:
            comp = await self.research_orchestrator.conduct_comprehensive_research(
                niche=goal.niche,
                goal=f"Grow {goal.target_metric} by {int(goal.target_increase*100)}% in {goal.timeline_days} days",
            )
            research_insights: List[ResearchInsight] = comp.get("raw_insights", [])  # type: ignore[assignment]
            synthesized_from_orchestrator = comp.get("synthesized", [])
        except Exception as e:
            logger.exception("Comprehensive research failed, falling back to raw: %s", e)
            research_insights = []
            synthesized_from_orchestrator = []
        if not research_insights:
            research_insights = await self.conduct_multi_source_research(goal)

        # Phase 1.5: Synthesize multi-source insights into patterns
        synthesized_insights = self.synthesize_insights(research_insights)

        # Phase 2: Strategy synthesis using OpenManus reasoning
        strategy = await self.synthesize_growth_strategy(goal, research_insights)

        # Phase 3: Generate specific recommendations
        content_plan = await self.generate_content_recommendations(goal, strategy)
        automation_tasks = await self.generate_automation_tasks(goal, strategy)

        # Phase 4: Create approval-required plan
        growth_plan: Dict[str, Any] = {
            "research_summary": self.summarize_research(research_insights),
            "content_calendar": content_plan,
            "automation_plan": automation_tasks,
            "timeline": self.create_timeline(goal),
            "success_metrics": self.define_success_metrics(goal),
            "synthesized_insights": [
                {
                    "pattern": s.pattern,
                    "confidence": s.confidence,
                    "metadata": s.metadata,
                    "evidence": [
                        {
                            "source": (getattr(e, "source", None) if not isinstance(e, dict) else e.get("source") or e.get("provider") or e.get("origin")),
                            "insight": (getattr(e, "insight", None) if not isinstance(e, dict) else e.get("insight") or e.get("text") or e.get("summary") or str(e)),
                            "confidence": (getattr(e, "confidence", None) if not isinstance(e, dict) else e.get("confidence")),
                            "metadata": (getattr(e, "metadata", None) if not isinstance(e, dict) else e.get("metadata")),
                        }
                        for e in s.evidence
                    ],
                }
                for s in synthesized_insights
            ],
            "requires_user_approval": True,
            "orchestrator_synthesized": synthesized_from_orchestrator,
        }
        logger.info("process_growth_goal done in %.2fs; insights=%d", time.time()-t0, len(research_insights))
        return growth_plan

    async def execute_approved_plan(self, approved_plan: Dict[str, Any]) -> Dict[str, Any]:
        """Execute user-approved automation tasks via Riona.

        NOTE: This is a placeholder; wire to Riona HTTP API or SDK when ready.
        """
        # TODO: Implement Riona integration for task execution
        execution_results: Dict[str, Any] = {
            "tasks_completed": [],
            "tasks_failed": [],
            "metrics_updated": {},
            "next_actions": [],
        }
        return execution_results

    # --------------------------- Research ---------------------------

    async def conduct_multi_source_research(self, goal: GrowthGoal) -> List[ResearchInsight]:
        """Parallel research across multiple platforms via registered tools."""
        # Use the modular orchestrator with smart routing across providers
        insights = await self.research_orchestrator.conduct_raw_insights(
            niche=goal.niche,
            goal=f"Grow {goal.target_metric} by {int(goal.target_increase*100)}% in {goal.timeline_days} days",
            research_types=["trends", "trends_realtime", "strategies", "success_stories", "creators"],
        )
        # As a simple backup, if nothing returned, call basic Tavily explicitly
        if not insights:
            base_queries = [
                f"{goal.niche} Instagram growth success stories",
                f"how to grow {goal.niche} Instagram account 2025",
                f"{goal.niche} influencer strategies that work",
                f"Instagram {goal.niche} content that gets engagement",
                f"best times to post {goal.niche} Instagram content",
            ]
            research_queries = self.query_optimizer.expand(base_queries, goal.niche)
            insights = await self.research_with_tavily(research_queries)
        return insights

    async def research_with_tavily(self, queries: List[str]) -> List[ResearchInsight]:
        tavily = TavilyResearchTool()
        return await tavily.research(queries)

    # --------------------------- Synthesis ---------------------------

    def synthesize_insights(self, insights: List[ResearchInsight]):
        """Collapse raw insights into patterns with confidence and metadata."""
        return self.synthesis.synthesize(insights)

    # --------------------------- Strategy ---------------------------

    async def synthesize_growth_strategy(self, goal: GrowthGoal, insights: List[ResearchInsight]) -> Dict[str, Any]:
        """Use OpenManus/Manus to reason about research and create strategy."""
        # Build a readable research context that tolerates dicts or objects
        ctx_lines: List[str] = []
        for i in insights:
            try:
                src = getattr(i, "source", None)
                ins = getattr(i, "insight", None)
                if src is None or ins is None:
                    if isinstance(i, dict):
                        src = i.get("source") or i.get("provider") or i.get("origin") or "source"
                        ins = i.get("insight") or i.get("text") or i.get("summary") or str(i)
                ctx_lines.append(f"- {src}: {ins}")
            except Exception:
                ctx_lines.append(f"- {str(i)}")
        research_context = "\n".join(ctx_lines)

        current_followers = goal.current_followers or 0
        target_total = int(current_followers * (1 + goal.target_increase)) if current_followers else None

        strategy_prompt = f"""
        Based on comprehensive research from multiple sources, create a detailed Instagram growth strategy.

        GOAL: Grow {goal.niche} Instagram account by {goal.target_increase*100:.0f}% ({current_followers} to {target_total}) in {goal.timeline_days} days.

        RESEARCH INSIGHTS:
        {research_context}

        Create a strategic plan that includes:
        1. Content themes and posting frequency
        2. Optimal posting times and content types
        3. Hashtag strategy based on current trends
        4. Engagement tactics that work for this niche
        5. Safe automation actions with daily limits
        6. Success milestones and tracking metrics

        Focus on actionable, Instagram-compliant strategies that combine user content creation with safe automation.
        """

        try:
            strategy_text = await self.manus_agent.ask(strategy_prompt)
            return {"strategy_text": strategy_text, "insights_used": insights}
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.exception("LLM synthesis failed, using heuristic fallback: %s", e)
            # Heuristic fallback: derive a basic strategy from insights and goal
            # Summarize top themes from insights
            themes: Dict[str, int] = {}
            def _safe_text(x: Any) -> str:
                try:
                    t = getattr(x, "insight", None)
                    if t:
                        return str(t)
                    if isinstance(x, dict):
                        return str(x.get("insight") or x.get("text") or x.get("summary") or x)
                except Exception:
                    pass
                return str(x)

            for i in insights[:50]:
                t = _safe_text(i).lower()
                for k in ["reel", "carousel", "hashtag", "engagement", "comment", "follow", "post time", "story", "collab", "ugc"]:
                    if k in t:
                        themes[k] = themes.get(k, 0) + 1

            top_themes = sorted(themes.items(), key=lambda kv: kv[1], reverse=True)[:5]
            lines: List[str] = []
            lines.append(f"Fallback strategy for {goal.niche} over {goal.timeline_days} days targeting {int(goal.target_increase*100)}% growth")
            lines.append("")
            lines.append("Content Plan:")
            lines.append("- Post 3x per week: mix of Reels and Carousels; keep hooks strong in first 2s")
            lines.append("- Daily Story: poll or question to drive replies")
            lines.append("- Themes observed in research: " + ", ".join(k for k, _ in top_themes) if top_themes else "- Generic IG growth best-practices")
            lines.append("")
            lines.append("Hashtag & Timing:")
            lines.append("- Use 5-8 niche hashtags + 2 broad; rotate sets; avoid banned tags")
            lines.append("- Post at 11am-1pm and 6-9pm local; test and log results")
            lines.append("")
            lines.append("Engagement & Safety:")
            lines.append("- Like 30-50 posts/day in niche; leave 5-10 genuine comments")
            lines.append("- Follow 15-25 relevant creators/day; unfollow after 7-10 days if no reciprocity")
            lines.append("- Respect IG limits; avoid bursts and automation on new accounts")
            lines.append("")
            lines.append("Milestones & Metrics:")
            lines.append("- Track: saves, shares, reach, follows/day; review weekly and double-down on winners")

            return {"strategy_text": "\n".join(lines), "insights_used": insights, "fallback": True}

    # --------------------------- Recommendations ---------------------------

    async def generate_content_recommendations(self, goal: GrowthGoal, strategy: Dict[str, Any]) -> List[ContentRecommendation]:
        """Generate a lightweight content calendar from the strategy text.

        Placeholder heuristic: 3 posts/week, mix of reels and carousels, themed to niche.
        """
        plan: List[ContentRecommendation] = []
        weeks = max(1, goal.timeline_days // 7)
        per_week = 3
        total_posts = weeks * per_week
        for i in range(total_posts):
            post_type = "reel" if i % 2 == 0 else "carousel"
            plan.append(ContentRecommendation(
                post_type=post_type,
                theme=f"{goal.niche} theme #{i+1}",
                caption_template=f"Quick tip #{i+1} about {goal.niche}. CTA: save & share!",
                hashtags=[goal.niche, "instagramgrowth", "reels", "contentcreator"],
                best_time="18:00 local",
            ))
        return plan

    async def generate_automation_tasks(self, goal: GrowthGoal, strategy: Dict[str, Any]) -> List[AutomationTask]:
        """Generate safe automation tasks aligned with the growth goal.

        Placeholder heuristic: modest daily limits; criteria aimed at the niche.
        """
        tasks: List[AutomationTask] = [
            AutomationTask(
                action_type="like",
                target_criteria={"hashtag": goal.niche, "recent": True},
                daily_limit=50,
            ),
            AutomationTask(
                action_type="comment",
                target_criteria={"hashtag": goal.niche, "recent": True},
                daily_limit=10,
                message_template="Love this! Great {niche} content 🔥",
            ),
            AutomationTask(
                action_type="follow",
                target_criteria={"followers_of": f"top_{goal.niche}_creators"},
                daily_limit=25,
            ),
        ]
        return tasks

    # --------------------------- Packaging ---------------------------

    def summarize_research(self, insights: List[ResearchInsight]) -> str:
        bullets: List[str] = []
        for i in insights[:10]:
            try:
                # Handle dataclass-like objects first
                source = getattr(i, "source", None)
                insight = getattr(i, "insight", None)
                if source is not None and insight is not None:
                    bullets.append(f"- [{source}] {insight}")
                    continue
                # Fallback: handle dicts
                if isinstance(i, dict):
                    src = i.get("source") or i.get("provider") or i.get("origin") or "source"
                    ins = i.get("insight") or i.get("text") or i.get("summary") or str(i)
                    bullets.append(f"- [{src}] {ins}")
                    continue
                # Last resort: string representation
                bullets.append(f"- {str(i)}")
            except Exception:
                bullets.append(f"- {str(i)}")
        return "\n".join(bullets)

    def create_timeline(self, goal: GrowthGoal) -> Dict[str, Any]:
        return {
            "days": goal.timeline_days,
            "milestones": [
                {"day": 0, "note": "Start"},
                {"day": max(1, goal.timeline_days // 3), "note": "Checkpoint 1"},
                {"day": max(2, 2 * goal.timeline_days // 3), "note": "Checkpoint 2"},
                {"day": goal.timeline_days, "note": "Final review"},
            ],
        }

    def define_success_metrics(self, goal: GrowthGoal) -> Dict[str, Any]:
        metrics: Dict[str, Any] = {
            "target_metric": goal.target_metric,
            "target_increase": goal.target_increase,
            "timeline_days": goal.timeline_days,
        }
        if goal.current_followers is not None:
            metrics["current_followers"] = goal.current_followers
            metrics["target_followers"] = int(goal.current_followers * (1 + goal.target_increase))
        return metrics
