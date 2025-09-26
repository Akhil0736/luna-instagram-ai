import sys
import os
from typing import List, Dict, Any

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from prompts.prompt_manager import LunaPromptManager


class LunaPromptTester:
    def __init__(self) -> None:
        self.prompt_manager = LunaPromptManager()
        self.test_results: Dict[str, Dict[str, Any]] = {}

    def _record_result(self, name: str, passed: bool, details: str = "") -> None:
        self.test_results[name] = {
            "passed": passed,
            "details": details,
        }

    def run_all_tests(self) -> None:
        """Run comprehensive testing suite for all Luna modules."""
        print("🧪 LUNA AI PROMPT TESTING FRAMEWORK")
        print("=" * 50)

        # Test 1: Query Type Detection
        self.test_query_detection()

        # Test 2: Consultation Methodology
        self.test_consultation_framework()

        # Test 3: Content Strategy (SPARK)
        self.test_content_strategy()

        # Test 4: Safety Compliance
        self.test_safety_compliance()

        # Test 5: Engagement Optimization (CONNECT)
        self.test_engagement_optimization()

        # Test 6: Audience Analysis (DECODE)
        self.test_audience_analysis()

        # Test 7: Competitive Intelligence (INTEL)
        self.test_competitive_intelligence()

        # Test 8: Growth Acceleration (ROCKET)
        self.test_growth_acceleration()

        # Test 9: Realtime Research Integration
        self.test_realtime_research()

        # Test 10: Prompt Manager Orchestration
        self.test_prompt_orchestration()

        # Generate Test Report
        self.generate_test_report()

    def test_query_detection(self) -> None:
        """Test Perplexity-inspired query type detection."""
        print("\n🎯 Testing Query Type Detection System...")

        test_queries = [
            {
                "query": "I'm a fitness coach with 2,500 followers and want to grow to 10K in 3 months. My engagement rate is around 4% and I post 3 times per week. What strategy should I follow?",
                "expected_type": "strategy_consultation",
                "expected_confidence": 90,
            },
            {
                "query": "I need content ideas for my travel blog. What should I post to get more engagement?",
                "expected_type": "content_creation",
                "expected_confidence": 75,
            },
            {
                "query": "My reach suddenly dropped 60% last week and I think I might be shadow-banned. Help!",
                "expected_type": "growth_troubleshooting",
                "expected_confidence": 95,
            },
            {
                "query": "Can you analyze my competitor accounts and tell me what they're doing better?",
                "expected_type": "competitor_research",
                "expected_confidence": 85,
            },
            {
                "query": "What are the trending content formats on Instagram right now?",
                "expected_type": "trend_analysis",
                "expected_confidence": 80,
            },
        ]

        passes = 0
        for i, test in enumerate(test_queries):
            result = self.prompt_manager.detect_query_type(test["query"])
            detected_type = result.get("type", "unknown")
            detected_confidence = result.get("confidence", 0)

            type_pass = detected_type == test["expected_type"]
            confidence_pass = detected_confidence >= test["expected_confidence"] - 20
            test_pass = type_pass and confidence_pass
            passes += int(test_pass)

            status = "✅ PASS" if test_pass else "❌ FAIL"
            print(f"  Test {i + 1}: {status}")
            print(f"    Query: {test['query'][:60]}...")
            print(
                f"    Expected: {test['expected_type']} ({test['expected_confidence']}%)"
            )
            print(f"    Detected: {detected_type} ({detected_confidence}%)")

        all_passed = passes == len(test_queries)
        self._record_result(
            "query_detection",
            all_passed,
            f"{passes}/{len(test_queries)} detections matched expectations",
        )

    def test_consultation_framework(self) -> None:
        """Test STRATEGIC consultation methodology."""
        print("\n🎯 Testing Consultation Methodology (STRATEGIC Framework)...")

        test_case = {
            "query": "I run a small bakery Instagram account with 850 followers. I want to increase local customers but don't know what content works. I can post once daily and have about 30 minutes for Instagram each day.",
            "expected_elements": [
                "Instagram Growth Strategy Analysis",
                "Current Position Analysis",
                "Recommended Strategic Framework",
                "Implementation Roadmap",
                "Immediate Actions",
                "Weekly Focus",
                "Monthly Goals",
            ],
        }

        response = self.prompt_manager.generate_consultation_response(test_case["query"])

        missing_elements = [
            element
            for element in test_case["expected_elements"]
            if element.lower() not in response.lower()
        ]

        if not missing_elements:
            print("  ✅ PASS - All required consultation elements present")
            self._record_result("consultation_framework", True)
        else:
            print(f"  ❌ FAIL - Missing elements: {missing_elements}")
            self._record_result(
                "consultation_framework",
                False,
                f"Missing elements: {', '.join(missing_elements)}",
            )

        self.test_confidence_responses()

    def test_confidence_responses(self) -> None:
        """Test Cluely-inspired confidence thresholds."""
        print("    Testing confidence-based response adaptation...")

        confidence_tests = [
            {
                "scenario": "High confidence (90%+)",
                "query": "I have 5K followers, post daily, want to reach 10K in 2 months, budget $200/month",
                "expected_response_type": "comprehensive_strategy",
            },
            {
                "scenario": "Medium confidence (50-90%)",
                "query": "Help me grow my account",
                "expected_response_type": "clarification_questions",
            },
            {
                "scenario": "Low confidence (<50%)",
                "query": "Instagram",
                "expected_response_type": "discovery_mode",
            },
        ]

        passes = 0
        for test in confidence_tests:
            response = self.prompt_manager.assess_confidence_and_respond(test["query"])
            confidence = response.get("confidence", 0)
            response_type = response.get("response_type", "unknown")

            if confidence >= 90 and test["expected_response_type"] == "comprehensive_strategy":
                passes += 1
                status = "✅"
            elif 50 <= confidence < 90 and test["expected_response_type"] == "clarification_questions":
                passes += 1
                status = "✅"
            elif confidence < 50 and test["expected_response_type"] == "discovery_mode":
                passes += 1
                status = "✅"
            else:
                status = "❌"

            print(
                f"    {status} {test['scenario']} -> confidence {confidence}% ({response_type})"
            )

        self._record_result(
            "confidence_responses",
            passes == len(confidence_tests),
            f"{passes}/{len(confidence_tests)} scenarios matched",
        )

    def test_content_strategy(self) -> None:
        """Test SPARK Method content strategy."""
        print("\n🎯 Testing Content Strategy (SPARK Method)...")

        test_case = {
            "query": "I'm a personal trainer and my posts get low engagement. I mostly share workout videos but they don't seem to connect with my audience. Need help with content planning.",
            "expected_spark_elements": [
                "Situation Analysis",
                "Pillar Definition",
                "Audience Alignment",
                "Refresh & Repurpose",
                "KPI Tracking",
            ],
        }

        response = self.prompt_manager.generate_content_strategy(test_case["query"])

        spark_score = sum(
            1
            for element in test_case["expected_spark_elements"]
            if element.lower() in response.lower()
        )

        if spark_score >= 4:
            print(f"  ✅ PASS - SPARK elements present ({spark_score}/5)")
            self._record_result("content_strategy", True, f"{spark_score}/5 elements found")
        else:
            print(f"  ❌ FAIL - Missing SPARK elements ({spark_score}/5)")
            self._record_result("content_strategy", False, f"{spark_score}/5 elements")

    def test_safety_compliance(self) -> None:
        """Test safety and compliance protocols."""
        print("\n🎯 Testing Safety & Compliance Module...")

        safety_scenarios = [
            "I think I'm shadow-banned, my reach dropped 70%",
            "Can I use engagement pods to boost my posts?",
            "How many hashtags should I use to avoid penalties?",
        ]

        passes = 0
        for scenario in safety_scenarios:
            response = self.prompt_manager.generate_safety_response(scenario)

            safety_elements = ["risk", "compliance", "violation", "safe", "protocol"]
            safety_score = sum(
                1 for element in safety_elements if element in response.lower()
            )

            status = "✅" if safety_score >= 3 else "❌"
            passes += int(safety_score >= 3)
            print(f"  {status} Safety response quality for: {scenario[:40]}...")

        self._record_result(
            "safety_compliance",
            passes == len(safety_scenarios),
            f"{passes}/{len(safety_scenarios)} scenarios met safety threshold",
        )

    def test_engagement_optimization(self) -> None:
        """Test CONNECT Method engagement optimization."""
        print("\n🎯 Testing Engagement Optimization (CONNECT Method)...")

        test_query = "My followers don't engage with my posts. How do I build a community?"
        response = self.prompt_manager.generate_engagement_strategy(test_query)

        connect_elements = [
            "Community Mapping",
            "Outreach & Interaction",
            "Nurture & Value",
            "Network Amplification",
            "Engagement Analytics",
            "Continuous Improvement",
            "Trust & Loyalty",
        ]

        connect_score = sum(
            1
            for element in connect_elements
            if element.lower().replace(" ", "") in response.lower().replace(" ", "")
        )

        if connect_score >= 5:
            print(f"  ✅ PASS - CONNECT framework implemented ({connect_score}/7)")
            self._record_result(
                "engagement_optimization",
                True,
                f"{connect_score}/7 CONNECT pillars detected",
            )
        else:
            print(f"  ❌ FAIL - CONNECT framework incomplete ({connect_score}/7)")
            self._record_result(
                "engagement_optimization",
                False,
                f"{connect_score}/7 CONNECT pillars",
            )

    def test_audience_analysis(self) -> None:
        """Test DECODE Method audience analysis."""
        print("\n🎯 Testing Audience Analysis (DECODE Method)...")

        test_query = "Can you analyze my audience? I have 3K followers but don't know who they are or what they want."
        response = self.prompt_manager.generate_audience_analysis(test_query)

        decode_elements = [
            "Demographic Segmentation",
            "Engagement Behavior Analysis",
            "Content Preference Identification",
            "Opportunity Mapping",
            "Deep Psychographic Profiling",
            "Evolution Tracking",
        ]

        decode_score = sum(
            1 for element in decode_elements if element.lower() in response.lower()
        )

        if decode_score >= 4:
            print(f"  ✅ PASS - DECODE analysis comprehensive ({decode_score}/6)")
            self._record_result(
                "audience_analysis",
                True,
                f"{decode_score}/6 DECODE pillars present",
            )
        else:
            print(f"  ❌ FAIL - DECODE analysis incomplete ({decode_score}/6)")
            self._record_result(
                "audience_analysis",
                False,
                f"{decode_score}/6 DECODE pillars",
            )

    def test_competitive_intelligence(self) -> None:
        """Test INTEL Method competitive intelligence."""
        print("\n🎯 Testing Competitive Intelligence (INTEL Method)...")

        test_query = "I want to analyze my competitors in the fitness niche. Who should I watch and what should I learn from them?"
        response = self.prompt_manager.generate_competitive_analysis(test_query)

        intel_elements = [
            "Identify Key Players",
            "Navigate Competitor Strategies",
            "Track Performance Metrics",
            "Evaluate Content Gaps",
            "Leverage Differentiation",
        ]

        intel_score = sum(
            1 for element in intel_elements if element.lower() in response.lower()
        )

        if intel_score >= 4:
            print(f"  ✅ PASS - INTEL framework operational ({intel_score}/5)")
            self._record_result(
                "competitive_intelligence",
                True,
                f"{intel_score}/5 INTEL pillars present",
            )
        else:
            print(f"  ❌ FAIL - INTEL framework incomplete ({intel_score}/5)")
            self._record_result(
                "competitive_intelligence",
                False,
                f"{intel_score}/5 INTEL pillars",
            )

    def test_growth_acceleration(self) -> None:
        """Test ROCKET Method growth acceleration."""
        print("\n🎯 Testing Growth Acceleration (ROCKET Method)...")

        test_query = "I want to scale my account rapidly from 5K to 50K followers. What's the fastest sustainable approach?"
        response = self.prompt_manager.generate_growth_acceleration(test_query)

        rocket_elements = [
            "Rapid Content Pipeline",
            "Omni-Channel Amplification",
            "Collaboration Strategies",
            "KPI Optimization",
            "Exponential Experimentation",
            "Tracking & Iteration",
        ]

        rocket_score = sum(
            1 for element in rocket_elements if element.lower() in response.lower()
        )

        if rocket_score >= 5:
            print(f"  ✅ PASS - ROCKET method ready for launch ({rocket_score}/6)")
            self._record_result(
                "growth_acceleration",
                True,
                f"{rocket_score}/6 ROCKET pillars present",
            )
        else:
            print(f"  ❌ FAIL - ROCKET method incomplete ({rocket_score}/6)")
            self._record_result(
                "growth_acceleration",
                False,
                f"{rocket_score}/6 ROCKET pillars",
            )

    def test_realtime_research(self) -> None:
        """Test Perplexity-inspired research integration."""
        print("\n🎯 Testing Realtime Research Integration...")

        test_query = "What are the最新 Instagram algorithm changes and how should I adapt my strategy?"
        response = self.prompt_manager.generate_research_response(test_query)

        citation_markers = ["[1]", "[2]", "[3]"]
        citations_found = sum(1 for marker in citation_markers if marker in response)

        research_elements = ["source", "research", "analysis", "validated", "evidence", "community"]
        research_score = sum(1 for element in research_elements if element in response.lower())

        passed = citations_found >= 2 and research_score >= 3
        status = "✅ PASS" if passed else "❌ FAIL"
        print(
            f"  {status} - Research integration ({citations_found} citations, {research_score}/6 elements)"
        )
        self._record_result(
            "realtime_research",
            passed,
            f"Citations: {citations_found}, elements: {research_score}/6",
        )

    def test_prompt_orchestration(self) -> None:
        """Test master prompt manager orchestration."""
        print("\n🎯 Testing Prompt Manager Orchestration...")

        orchestration_tests = [
            {
                "query": "I need a complete Instagram strategy for my fitness business",
                "expected_modules": [
                    "consultation_methodology",
                    "instagram_expert",
                    "content_strategy",
                ],
            },
            {
                "query": "My account got restricted, help me recover",
                "expected_modules": ["safety_compliance", "growth_acceleration"],
            },
            {
                "query": "Analyze my top 3 competitors in the beauty niche",
                "expected_modules": [
                    "competitive_intelligence",
                    "realtime_research",
                ],
            },
        ]

        orchestration_score = 0
        for test in orchestration_tests:
            result = self.prompt_manager.orchestrate_response(test["query"])

            modules_activated = result.get("modules_used", [])
            expected_modules = test["expected_modules"]

            if any(module in modules_activated for module in expected_modules):
                orchestration_score += 1
                print(f"  ✅ Orchestration test passed: {test['query'][:40]}...")
            else:
                print(f"  ❌ Orchestration test failed: {test['query'][:40]}...")

        passed = orchestration_score >= 2
        self._record_result(
            "prompt_orchestration",
            passed,
            f"{orchestration_score}/{len(orchestration_tests)} orchestration scenarios",
        )

    def generate_test_report(self) -> None:
        """Generate comprehensive test results report."""
        print("\n" + "=" * 50)
        print("🎊 LUNA AI TESTING COMPLETE")
        print("=" * 50)

        passed_tests = [name for name, result in self.test_results.items() if result["passed"]]
        failed_tests = [name for name, result in self.test_results.items() if not result["passed"]]

        print("\n📊 TEST SUMMARY:")
        for name, result in self.test_results.items():
            status = "PASS" if result["passed"] else "FAIL"
            detail_text = f" - {result['details']}" if result.get("details") else ""
            print(f"- {name}: {status}{detail_text}")

        print("\n🚀 NEXT STEPS:")
        print("- Review any failed tests and refine prompts")
        print("- Test with real Instagram account data")
        print("- Validate memory persistence across sessions")
        print("- Optimize response times and quality")

        if failed_tests:
            print("\n❌ Some tests failed. Please address the issues above.")
        else:
            print("\n🌙 Luna AI is ready for deployment! All tests passed.")


if __name__ == "__main__":
    tester = LunaPromptTester()
    tester.run_all_tests()
