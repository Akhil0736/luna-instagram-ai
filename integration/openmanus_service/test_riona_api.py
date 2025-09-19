import asyncio
import httpx
import json

async def test_riona_api_endpoints():
    """Test all new Riona API endpoints"""
    
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        print("🌙 Testing Luna → Riona API Integration")
        print("="*50)
        
        # Test 1: Health check
        print("\n1️⃣ Testing Riona health check...")
        try:
            response = await client.get(f"{base_url}/luna/riona/health")
            print(f"✅ Health check: {response.status_code}")
            if response.status_code == 200:
                print(f"Response: {response.json()}")
            else:
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
        
        # Test 2: Complete system info
        print("\n2️⃣ Testing complete system info...")
        try:
            response = await client.get(f"{base_url}/luna/system/complete-info")
            print(f"✅ System info: {response.status_code}")
            if response.status_code == 200:
                system_info = response.json()
                print(f"Version: {system_info.get('version', 'N/A')}")
                print(f"Riona Integration: {system_info.get('components', {}).get('riona_integration', 'N/A')}")
            else:
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ System info failed: {e}")
        
        # Test 3: Basic Luna endpoints (existing)
        print("\n3️⃣ Testing existing Luna system...")
        try:
            response = await client.get(f"{base_url}/luna/system/info")
            print(f"✅ Luna system: {response.status_code}")
            if response.status_code == 200:
                info = response.json()
                print(f"Luna Status: {info.get('luna_status', 'N/A')}")
            else:
                print(f"Response: {response.text}")
        except Exception as e:
            print(f"❌ Luna system test failed: {e}")
        
        # Test 4: Manual strategy execution
        print("\n4️⃣ Testing manual strategy execution...")
        try:
            strategy_request = {
                "user_id": "api_test_user",
                "niche": "fitness coaching",
                "consultation_context": "API endpoint test",
                "strategy": {
                    "target_audience": ["fitness_enthusiasts", "gym_owners"],
                    "hashtag_strategy": ["#fitness", "#coaching", "#transformation"],
                    "engagement_tactics": ["like_fitness_posts", "follow_fitness_accounts"]
                },
                "execution_plan": {
                    "daily_likes": 40,
                    "daily_follows": 15,
                    "daily_comments": 5
                }
            }
            
            response = await client.post(
                f"{base_url}/luna/riona/execute-strategy",
                json=strategy_request
            )
            print(f"✅ Strategy execution: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"🎯 Execution ID: {result['execution_id']}")
                    print(f"📋 Tasks queued: {result['tasks_queued']}")
                    print(f"🛡️ Tasks filtered: {result['tasks_filtered']}")
                    print(f"⏰ Estimated completion: {result['estimated_completion']}")
                    
                    execution_id = result['execution_id']
                    
                    # Test 5: Check execution status
                    print("\n5️⃣ Testing execution status...")
                    await asyncio.sleep(2)  # Wait a bit for execution to start
                    
                    status_response = await client.get(f"{base_url}/luna/riona/execution-status/{execution_id}")
                    print(f"✅ Status check: {status_response.status_code}")
                    
                    if status_response.status_code == 200:
                        status = status_response.json()
                        print(f"Status: {status['status']}")
                        print(f"Progress: {status['progress_percentage']:.1f}%")
                        print(f"Tasks: {status['completed_tasks']}/{status['total_tasks']}")
                    else:
                        print(f"Status response: {status_response.text}")
                        
                else:
                    print(f"❌ Execution failed: {result.get('error')}")
            else:
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Manual strategy execution failed: {e}")

if __name__ == "__main__":
    print("🌙 Starting Luna → Riona API Integration Tests...")
    print("Server should be running on localhost:8000")
    print()
    
    asyncio.run(test_riona_api_endpoints())
