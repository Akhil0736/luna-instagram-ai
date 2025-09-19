import asyncio
import httpx
import json

async def test_riona_task_execution():
    """Test Riona task execution system"""
    
    base_url = "http://localhost:8000"
    
    print("🚀 Testing Riona Task Execution System")
    print("="*60)
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        
        # Test 1: Test engagement system
        print("\n1️⃣ Testing engagement system...")
        try:
            response = await client.post(f"{base_url}/luna/execution/test-engagement")
            print(f"✅ Engagement test: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Test Status: {result['test_status']}")
                print(f"Engagement Result: {result.get('engagement_result', {}).get('task_type', 'N/A')}")
                
                if result.get('executor_stats'):
                    stats = result['executor_stats']
                    print(f"Execution Stats: {stats['session_stats']['successful_actions']} successful actions")
            
        except Exception as e:
            print(f"❌ Engagement test failed: {e}")
        
        # Test 2: Manual task execution
        print("\n2️⃣ Testing manual task execution...")
        try:
            task_request = {
                "user_id": "manual_test_user",
                "task_type": "engagement_like",
                "task_data": {
                    "post_urls": [
                        "https://instagram.com/p/test1",
                        "https://instagram.com/p/test2",
                        "https://instagram.com/p/test3"
                    ],
                    "target_count": 3
                },
                "user_credentials": {
                    "username": "test_user",
                    "password": "test_pass"
                }
            }
            
            response = await client.post(
                f"{base_url}/luna/execution/execute-task",
                json=task_request
            )
            print(f"✅ Manual task execution: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"Task Type: {result['task_type']}")
                print(f"Success: {result['success']}")
                
                execution_result = result.get('execution_result', {})
                if execution_result.get('total_attempts'):
                    print(f"Attempts: {execution_result['total_attempts']}")
                    print(f"Success Rate: {execution_result.get('success_rate', 0):.2%}")
            
        except Exception as e:
            print(f"❌ Manual task execution failed: {e}")
        
        # Test 3: Audience research
        print("\n3️⃣ Testing audience research...")
        try:
            research_request = {
                "user_id": "research_test_user",
                "task_type": "audience_research",
                "task_data": {
                    "competitors": ["competitor1", "competitor2"],
                    "depth": "basic"
                },
                "user_credentials": {
                    "username": "research_user",
                    "password": "research_pass"
                }
            }
            
            response = await client.post(
                f"{base_url}/luna/execution/execute-task",
                json=research_request
            )
            print(f"✅ Audience research: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                execution_result = result.get('execution_result', {})
                
                if execution_result.get('targets_identified'):
                    print(f"Targets Identified: {execution_result['targets_identified']}")
                    print(f"Competitors Analyzed: {execution_result['competitors_analyzed']}")
            
        except Exception as e:
            print(f"❌ Audience research failed: {e}")
        
        # Test 4: Get executor statistics
        print("\n4️⃣ Testing executor statistics...")
        try:
            response = await client.get(f"{base_url}/luna/execution/executor-stats/manual_test_user")
            print(f"✅ Executor stats: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                stats = result.get('statistics', {})
                session_stats = stats.get('session_stats', {})
                
                print(f"Total Likes: {session_stats.get('total_likes', 0)}")
                print(f"Total Follows: {session_stats.get('total_follows', 0)}")
                print(f"Success Rate: {stats.get('success_rate', 0):.2%}")
                print(f"Actions/Minute: {stats.get('actions_per_minute', 0):.2f}")
        
        except Exception as e:
            print(f"❌ Executor stats failed: {e}")
    
    print("\n" + "="*60)
    print("🌙 Riona Task Execution Test Complete")

if __name__ == "__main__":
    print("🌙 Starting Riona Task Execution Tests...")
    print("Make sure your FastAPI server is running on localhost:8000")
    print()
    
    asyncio.run(test_riona_task_execution())
