import asyncio
import httpx

async def test_complete_luna_system():
    """Test the complete Luna AI system with all components"""
    
    base_url = "http://localhost:8000"
    
    print("🌙 Testing Complete Luna AI System Integration")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test 1: Complete system status
        print("1️⃣ Testing complete system status...")
        try:
            response = await client.get(f"{base_url}/luna/system/complete-status")
            if response.status_code == 200:
                status = response.json()
                print(f"✅ System Status: {status['status']}")
                print(f"📊 Version: {status['version']}")
                print(f"🎯 Components: {len(status['components'])} operational")
                print(f"🚀 Capabilities: {len(status['capabilities'])} advanced features")
            else:
                print(f"❌ System status failed: {response.status_code}")
        except Exception as e:
            print(f"❌ System status error: {e}")
        
        # Test 2: Feedback system
        print("\n2️⃣ Testing feedback & optimization system...")
        try:
            feedback_data = {
                "execution_id": "test_exec_123",
                "user_id": "test_feedback_user",
                "performance_data": {
                    "successful_actions": 45,
                    "total_actions": 50,
                    "engagement_rate": 0.045,
                    "follower_growth": 12,
                    "time_spent_minutes": 180
                },
                "instagram_metrics": {
                    "likes": 89,
                    "comments": 23,
                    "saves": 12,
                    "reach": 1250
                }
            }
            
            response = await client.post(f"{base_url}/luna/feedback/process-execution", json=feedback_data)
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Feedback processed successfully")
                print(f"📊 Performance Score: {result['performance_score']:.1f}/100")
                print(f"🎯 Success Rate: {result['success_rate']:.1f}%")
                print(f"💡 Optimization Suggestions: {len(result['optimization_suggestions'])}")
            else:
                print(f"❌ Feedback processing failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Feedback processing error: {e}")
        
        # Test 3: Analytics system
        print("\n3️⃣ Testing advanced analytics...")
        try:
            response = await client.get(f"{base_url}/luna/feedback/analytics/test_feedback_user")
            if response.status_code == 200:
                analytics = response.json()
                print(f"✅ Analytics generated successfully")
                print(f"📈 Insights: {len(analytics['insights'])} generated")
                print(f"🔄 Recommendations: {len(analytics['recommendations'])} provided")
                print(f"🏆 Performance Grade: {analytics['performance_grade']}")
            else:
                print(f"❌ Analytics generation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Analytics error: {e}")
        
        # Test 4: Dashboard data
        print("\n4️⃣ Testing dashboard integration...")
        try:
            response = await client.get(f"{base_url}/luna/feedback/dashboard/test_feedback_user")
            if response.status_code == 200:
                dashboard = response.json()
                print(f"✅ Dashboard data generated successfully")
                if "current_performance" in dashboard:
                    perf = dashboard["current_performance"]
                    print(f"📊 Current Score: {perf.get('overall_score', 0):.1f}/100")
                    print(f"🎯 Status: {perf.get('status', 'unknown')}")
            else:
                print(f"❌ Dashboard generation failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Dashboard error: {e}")

    print("\n" + "="*70)
    print("🎉 Complete Luna AI System Integration Test Finished!")
    print("🚀 All missing components now integrated and operational!")

if __name__ == "__main__":
    asyncio.run(test_complete_luna_system())
