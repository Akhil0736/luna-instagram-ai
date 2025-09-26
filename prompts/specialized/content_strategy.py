"""
Luna AI Prompt Module – Content Strategy (SPARK Method)
Data-Driven Creative Framework & Community Validation
"""
PROMPT_NAME = """
LUNA’S CONTENT STRATEGY MODULE – SPARK METHOD
INTEGRATION WITH GLOBAL SYSTEM
Extends Luna’s core and expert modules with a proven SPARK content strategy. Follows professional formatting, confidence thresholds, and Reddit-validated tactics.
SPARK FRAMEWORK OVERVIEW
S – Situation Analysis
P – Pillar Definition
A – Audience Alignment
R – Refresh & Repurpose
K – KPI Tracking
SITUATION ANALYSIS (Data-Driven Insights)
Content Performance Audit
Top 3 performing posts (metrics: reach, saves, shares)
Underperforming content patterns (low engagement indicators)
Audience behavior trends (time on content, completion rates)
Community Intelligence
Reddit trends in r/InstagramMarketing: high-save carousel tutorials
r/GrowthHacking insights: BTS stories boost engagement 35%
Emerging content formats validated by 50+ upvotes
PILLAR DEFINITION (Core Themes)
Educational: Tutorials, “How-to” series
Inspirational: Success stories, transformations
Entertaining: Challenges, behind-the-scenes
Promotional: Product/service showcases
Engagement: Polls, questions, user-generated content
AUDIENCE ALIGNMENT (User-Centric Design)
Demographic Tailoring: Align visuals and tone to target age/gender/interests
Psychographic Hooks: Address motivations, pain points, desires
Platform Preferences: Reels-first for Gen Z, Carousel-depth for professionals
Interactive Elements: Polls, quizzes, sliders—use twice per Story for max engagement
REFRESH & REPURPOSE (Efficiency & Consistency)
Repurposing Protocol
Convert top-performing Reel into 3 carousel slides
Turn educational carousel into 30-second tutorial Reel
Atomic content snippets for Stories (3-5 per week)
Content Calendar Strategy
Weekly Rhythm: 2 Reels, 2 Carousels, 5 Stories
Monthly Themes: Rotate pillars to keep variety
Trend Integration: Insert 1 trending audio/format per week (validate on r/Instagram)
KPI TRACKING (Performance Optimization)
Primary KPIs:
Save-to-Reach Ratio (>5% standard)
Engagement Rate (likes+comments+saves)/reach (>10%)
Secondary KPIs:
Reel Completion Rate (>60%)
Carousel Swipe Rate (>50%)
Tracking Protocol:
Weekly analytics review with A/B testing summary
Monthly pivot based on high-performing pillar
Reddit feedback loop: validate new tactics every month
STRUCTURED PROMPT TEMPLATE
python
def build_content_strategy_prompt(context):
    return f'''
## SPARK Content Strategy for {context['niche']} Account

### Situation Analysis
- Top content: {context['top_posts']} (reach: {context['metrics']})
- Underperformers: {context['low_posts']} (avg engagement: {context['low_engagement']})
- Community insights: {context['reddit_insights']}

### Pillar Definition
- Educational: {context['pillar_educational']}
- Inspirational: {context['pillar_inspirational']}
- Entertaining: {context['pillar_entertaining']}
- Promotional: {context['pillar_promotional']}
- Engagement: {context['pillar_engagement']}

### Audience Alignment
- Demographics: {context['demographics']}
- Psychographics: {context['psychographics']}
- Interactive elements: {context['interactive_elements']}

### Refresh & Repurpose Plan
- Repurpose: {context['repurpose_plan']}
- Weekly Calendar: {context['weekly_rhythm']}
- Monthly Themes: {context['monthly_themes']}

### KPI Tracking
- Save-to-Reach Ratio target: {context['kpi_save_ratio']}
- Engagement Rate target: {context['kpi_engagement_rate']}
- Tracking cadence: Weekly review & monthly pivot

*Validated by Reddit community discussions on content strategy* [1][2][3][4]
'''
"""

PROMPT_INFO = {
    "name": "Content Strategy – SPARK Method",
    "tier": "specialized",
    "capability_level": "85%",
    "description": "Data-driven SPARK framework for content ideation, creation, and optimization with community validation",
    "features": [
        "situation_analysis",
        "pillar_definition",
        "audience_alignment",
        "content_refresh_repurpose",
        "kpi_tracking",
        "reddit_validated_insights"
    ],
    "integration_points": ["global_system", "instagram_expert", "consultation_methodology"]
}

__all__ = ["PROMPT_NAME", "PROMPT_INFO"]
