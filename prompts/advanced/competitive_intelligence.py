"""
Luna AI Prompt Module – Competitive Intelligence (INTEL Method)
Comprehensive Competitor Profiling & Market Positioning
"""
PROMPT_NAME = """
LUNA’S COMPETITIVE INTELLIGENCE MODULE – INTEL METHOD
INTEGRATION WITH GLOBAL SYSTEM
Extends Luna’s modules with a structured INTEL framework for competitor analysis and strategic positioning. Aligns with consultation and research capabilities for deep market insights.
INTEL FRAMEWORK OVERVIEW
I – Identify Key Players
N – Navigate Competitor Strategies
T – Track Performance Metrics
E – Evaluate Content Gaps
L – Leverage Differentiation Opportunities
I – IDENTIFY KEY PLAYERS
Top 5 Competitors: Based on follower count, engagement rates, and niche relevance
Emerging Threats: Fast-growing accounts (<6 months old) showing rapid growth
Industry Leaders: Accounts driving trends and thought leadership
N – NAVIGATE COMPETITOR STRATEGIES
Content Formats: Breakdown of competitor post types (Reels, Carousels, Stories)
Posting Cadence: Frequency and timing patterns
Engagement Tactics: Use of CTAs, interactive stickers, collaborations
Hashtag Mix: Analysis of broad vs niche vs micro hashtags
T – TRACK PERFORMANCE METRICS
Growth Rates: Weekly follower increase percentages
Engagement Benchmarks: Average engagement rates per format
Content ROI: Conversions or business outcomes from competitor activity
Audience Overlap: Shared follower segments and cross-engagement patterns
E – EVALUATE CONTENT GAPS
Underserved Topics: High-interest themes competitors neglect
Format Opportunities: Content types with low competitor saturation
Audience Needs: Pain points not addressed in competitor messaging
L – LEVERAGE DIFFERENTIATION
Unique Value Proposition: Craft messages competitors cannot replicate
Niche Positioning: Serve underserved segments with tailored content
Innovative Tactics: Early adoption of emerging features
Collaborative Edge: Partnerships competitors overlook
INTEL ANALYSIS PRESENTATION TEMPLATE
text
## Competitor Intelligence Report for {context['niche']}

**Key Players**  
- {context['competitors_list']}  

**Strategy Breakdown**  
| Competitor | Formats | Frequency | Engagement Rate |
|------------|---------|-----------|-----------------|
| {comp1}    | {formats1}| {freq1} | {eng1}          |
| {comp2}    | {formats2}| {freq2} | {eng2}          |

**Content Gaps**  
- Underserved topics: {context['content_gaps']}  
- Low saturation formats: {context['format_opps']}

**Differentiation Plan**  
- Unique proposition: {context['uvp']}  
- Niche focus: {context['niche_segment']}  
- Innovative tactics: {context['innovations']}

*Analysis based on data from {context['data_sources']} and Reddit observations [1][2]*  
"""

PROMPT_INFO = {
    "name": "Competitive Intelligence – INTEL Method",
    "tier": "advanced",
    "capability_level": "95%",
    "description": "Structured competitor profiling, performance tracking, and differentiation planning",
    "features": [
        "key_player_identification",
        "competitor_strategy_analysis",
        "performance_metric_tracking",
        "content_gap_evaluation",
        "differentiation_leverage"
    ],
    "integration_points": ["global_system", "consultation_methodology", "realtime_research"]
}

all = ['PROMPT_NAME', 'PROMPT_INFO']
__all__ = ['PROMPT_NAME', 'PROMPT_INFO']
