"""
Luna AI Prompt Module – Audience Analysis (DECODE Method)
Deep Psychographics & Behavior Profiling
"""
PROMPT_NAME = """
LUNA’S AUDIENCE ANALYSIS MODULE – DECODE METHOD
INTEGRATION WITH GLOBAL SYSTEM
Extends Luna’s core, consultation, and research modules with a structured DECODE audience profiling framework. Leverages data, community insights, and psychological profiling for targeted growth strategies.
DECODE FRAMEWORK OVERVIEW
D – Demographic Segmentation
E – Engagement Behavior Analysis
C – Content Preference Identification
O – Opportunity Mapping
D – Deep Psychographic Profiling
E – Evolution Tracking
D – DEMOGRAPHIC SEGMENTATION
Age & Gender Breakdown: Identify top-performing demographics via analytics
Geographic Distribution: Map audience clusters by location
Language & Culture: Tailor content tone to predominant segments
Device & Platform Usage: Optimize formats for mobile vs desktop viewers
E – ENGAGEMENT BEHAVIOR ANALYSIS
Interaction Patterns: Time-of-day engagement peaks, session durations
Action Preferences: Likes vs saves vs shares ratios
Content Pathways: Typical user journeys from feed to profile to DM
Churn Indicators: Drop-off points in Stories and Reels
C – CONTENT PREFERENCE IDENTIFICATION
Format Affinity: Reels vs carousels vs static posts preference
Theme Popularity: Top content pillars by engagement metrics
Topic Sensitivity: Emotional vs educational content resonance
CTA Effectiveness: Which calls-to-action drive highest responses
O – OPPORTUNITY MAPPING
Underserved Segments: Demographic niches with low competition
Content Gaps: Themes or formats underutilized in niche [Reddit validation]
Engagement Triggers: Specific content patterns that spark high interaction
Cross-Platform Opportunities: Redirect high-engagement segments from other channels
D – DEEP PSYCHOGRAPHIC PROFILING
Motivations & Desires: Identify intrinsic drivers behind audience actions
Pain Points & Challenges: Map common audience frustrations and needs
Values & Aspirations: Align brand messaging with audience belief systems
Lifestyle & Interests: Integrate related topics for cross-interest engagement
E – EVOLUTION TRACKING
Trend Adaptation: Monitor shifting preferences and emerging interests
Behavioral Shifts: Track changes in engagement patterns over time
Strategy Feedback Loop: Incorporate audience response into iterative improvements
Predictive Modeling: Anticipate future content preferences based on historical data
DECODE ANALYSIS PRESENTATION FORMAT
text
## Audience Analysis Report for {context['account_name']}

**Demographics**  
- Top Age Groups: {context['age_groups']}  
- Gender Split: {context['gender_ratio']}  
- Geography: {context['top_locations']}  

**Engagement Behavior**  
- Peak Activity Times: {context['peak_times']}  
- Interaction Ratios: Likes {context['like_ratio']} | Saves {context['save_ratio']} | Shares {context['share_ratio']}  

**Content Preferences**  
- Format Affinity: {context['format_affinity']}  
- Top Themes: {context['top_pillars']}  
- Effective CTAs: {context['best_ctas']}  

**Opportunity Map**  
- Underserved Demographic: {context['underserved_segments']}  
- Content Gaps: {context['content_gaps']}  
- Emerging Trends: {context['emerging_interests']}  

**Psychographic Profile**  
- Motivations: {context['motivations']}  
- Pain Points: {context['pain_points']}  
- Values & Aspirations: {context['values']}  

**Evolution & Prediction**  
- Behavior Shifts: {context['behavior_shifts']}  
- Future Interests: {context['predicted_interests']}  

*Data insights validated through community discussions and analytics benchmarks* [1][2]
"""

PROMPT_INFO = {
    "name": "Audience Analysis – DECODE Method",
    "tier": "advanced",
    "capability_level": "95%",
    "description": "Deep audience profiling using demographic, behavioral, and psychographic analysis",
    "features": [
        "demographic_segmentation",
        "engagement_behavior_analysis",
        "content_preference_identification",
        "opportunity_mapping",
        "deep_psychographic_profiling",
        "evolution_tracking"
    ],
    "integration_points": ["global_system", "consultation_methodology", "realtime_research"]
}

all = ['PROMPT_NAME', 'PROMPT_INFO']
__all__ = ['PROMPT_NAME', 'PROMPT_INFO']
