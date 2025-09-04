from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Dict, List, Any, Optional

from openmanus.app.agent.manus import Manus

from integration.models import (
    GrowthGoal,
    ResearchInsight,
    ContentRecommendation,
    AutomationTask,
)
from integration.research_tools import ResearchTool, TavilyResearchTool


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
        # Register research tools; default to Tavily tool
        self.research_tools: List[ResearchTool] = research_tools or [TavilyResearchTool()]
        # Placeholder for later: an authenticated Riona client instance
        self.riona_client = None

    # --------------------------- Public API ---------------------------

    async def process_growth_goal(self, goal: GrowthGoal) -> Dict[str, Any]:
        """Main orchestration method that handles user growth goals."""
        # Phase 1: Multi-source research
        research_insights = await self.conduct_multi_source_research(goal)

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
            "requires_user_approval": True,
        }
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
        research_queries = [
            f"{goal.niche} Instagram growth success stories",
            f"how to grow {goal.niche} Instagram account 2025",
            f"{goal.niche} influencer strategies that work",
            f"Instagram {goal.niche} content that gets engagement",
            f"best times to post {goal.niche} Instagram content",
        ]

        # Run all tools in parallel and flatten insights
        tool_tasks = [tool.research(research_queries) for tool in self.research_tools]
        results = await asyncio.gather(*tool_tasks, return_exceptions=True)

        insights: List[ResearchInsight] = []
        for res in results:
            if isinstance(res, Exception):
                insights.append(ResearchInsight(
                    source="error",
                    insight=f"Research tool error: {res}",
                    confidence=0.2,
                ))
            else:
                insights.extend(res)

        # As a simple backup, if nothing returned, call Tavily explicitly
        if not insights:
            insights = await self.research_with_tavily(research_queries)
        return insights

    async def research_with_tavily(self, queries: List[str]) -> List[ResearchInsight]:
        tavily = TavilyResearchTool()
        return await tavily.research(queries)

    # --------------------------- Strategy ---------------------------

    async def synthesize_growth_strategy(self, goal: GrowthGoal, insights: List[ResearchInsight]) -> Dict[str, Any]:
        """Use OpenManus/Manus to reason about research and create strategy."""
        research_context = "\n".join([f"- {i.source}: {i.insight}" for i in insights])

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

        strategy_text = await self.manus_agent.ask(strategy_prompt)
        return {"strategy_text": strategy_text, "insights_used": insights}

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
        bullets = [f"- [{i.source}] {i.insight}" for i in insights[:10]]
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
