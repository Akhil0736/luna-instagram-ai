import asyncio
import httpx

async def test_scheduling_system():
    base_url = "http://localhost:8000"
    
    print("🕒 Testing Luna AI Humanized Scheduling System")
    print("="*50)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        
        # Test 1: Basic server connection
        print("\n1️⃣ Testing server connection...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✅ Server connection: {response.status_code}")
        except Exception as e:
            print(f"❌ Server connection failed: {e}")
            return
        
        # Test 2: Luna system info
        print("\n2️⃣ Testing Luna system...")
        try:
            response = await client.get(f"{base_url}/luna/system/info")
            print(f"✅ Luna system: {response.status_code}")
            if response.status_code == 200:
                info = response.json()
                print(f"Luna Status: {info.get('luna_status', 'Unknown')}")
        except Exception as e:
            print(f"❌ Luna system test failed: {e}")
        
        # Test 3: Try Riona health check
        print("\n3️⃣ Testing Riona integration...")
        try:
            response = await client.get(f"{base_url}/luna/riona/health")
            print(f"✅ Riona health: {response.status_code}")
            if response.status_code == 200:
                health = response.json()
                print(f"Riona Status: {health.get('message', 'Unknown')}")
        except Exception as e:
            print(f"❌ Riona integration test failed: {e}")
        
        # Test 4: Try scheduling endpoints (if available)
        print("\n4️⃣ Testing scheduling system...")
        try:
            response = await client.get(f"{base_url}/luna/system/scheduling-info")
            print(f"✅ Scheduling info: {response.status_code}")
            if response.status_code == 200:
                sched_info = response.json()
                print(f"Scheduling System: {sched_info.get('scheduling_system', 'Unknown')}")
        except Exception as e:
            print(f"❌ Scheduling system not available: {e}")
        
        print("\n" + "="*50)
        print("🌙 Luna AI System Test Complete")

if __name__ == "__main__":
    asyncio.run(test_scheduling_system())
