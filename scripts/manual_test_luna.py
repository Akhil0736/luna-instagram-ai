import requests
import json

BASE_URL = "http://localhost:8000"


def test_luna_endpoints():
    """Manual testing of Luna AI endpoints"""

    print("🧪 TESTING LUNA AI ENDPOINTS")
    print("=" * 50)

    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/luna/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 2: Strategy consultation
    print("\n2. Testing strategy consultation...")
    query_data = {
        "query": "I'm a fitness coach with 2,500 followers and want to grow to 10K in 3 months. What strategy should I follow?",
        "user_id": "test_user_fitness",
        "account_context": {
            "followers": 2500,
            "engagement_rate": 0.04,
            "niche": "fitness"
        }
    }

    try:
        response = requests.post(f"{BASE_URL}/luna/query", json=query_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Query Type: {data['query_type']}")
            print(f"Confidence: {data['confidence']}%")
            print(f"Modules Used: {data['modules_used']}")
            print(f"Response Preview: {data['response'][:200]}...")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Test 3: Content creation
    print("\n3. Testing content creation...")
    content_data = {
        "query": "Give me 5 Instagram Reel ideas for my travel account",
        "user_id": "test_user_travel",
        "account_context": {"niche": "travel"}
    }

    try:
        response = requests.post(f"{BASE_URL}/luna/query", json=content_data)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Query Type: {data['query_type']}")
            print(f"Response Preview: {data['response'][:200]}...")
    except Exception as e:
        print(f"Error: {e}")

    print("\n✅ Manual testing complete!")


if __name__ == "__main__":
    test_luna_endpoints()
