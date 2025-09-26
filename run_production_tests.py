#!/usr/bin/env python3
"""
Luna AI Production Test Runner
Runs comprehensive end-to-end tests against production deployment
"""

import os
import sys
import subprocess
import time
import signal
import requests
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def start_server():
    """Start the Luna AI server in background"""
    print("🚀 Starting Luna AI production server...")

    # Set test environment variables
    env = os.environ.copy()
    env.update({
        'JWT_SECRET_KEY': 'test-jwt-secret-key-for-production-testing',
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test-anon-key',
        'UPSTASH_REDIS_REST_URL': 'https://test.upstash.io',
        'UPSTASH_REDIS_REST_TOKEN': 'test-token',
        'ENVIRONMENT': 'testing'
    })

    # Start server
    server_process = subprocess.Popen(
        [sys.executable, 'main.py'],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        preexec_fn=os.setsid
    )

    # Wait for server to start
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get('http://localhost:8000/luna/health', timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully!")
                return server_process
        except:
            pass

        print(f"⏳ Waiting for server to start... (attempt {attempt + 1}/{max_attempts})")
        time.sleep(2)

    # If server didn't start, show logs and exit
    stdout, stderr = server_process.communicate()
    print("❌ Server failed to start!")
    print("STDOUT:", stdout.decode())
    print("STDERR:", stderr.decode())
    sys.exit(1)

def run_tests():
    """Run the production integration tests"""
    print("🧪 Running Luna AI Production Integration Tests...")

    # Set test environment
    os.environ['TEST_BASE_URL'] = 'http://localhost:8000'

    # Run pytest
    result = subprocess.run([
        sys.executable, '-m', 'pytest',
        'tests/test_production_integration.py',
        '-v', '--tb=short', '--maxfail=3'
    ], capture_output=True, text=True)

    print("Test Output:")
    print(result.stdout)
    if result.stderr:
        print("Errors:")
        print(result.stderr)

    return result.returncode == 0

def stop_server(server_process):
    """Stop the server process"""
    print("🛑 Stopping Luna AI server...")
    try:
        os.killpg(os.getpgid(server_process.pid), signal.SIGTERM)
        server_process.wait(timeout=10)
        print("✅ Server stopped successfully!")
    except:
        print("⚠️  Server may still be running, force killing...")
        try:
            server_process.kill()
        except:
            pass

def main():
    """Main test runner"""
    print("🌙 LUNA AI PRODUCTION INTEGRATION TEST SUITE")
    print("=" * 60)

    server_process = None

    try:
        # Start server
        server_process = start_server()

        # Wait a bit more for full initialization
        time.sleep(5)

        # Run tests
        test_success = run_tests()

        if test_success:
            print("\n🎉 ALL PRODUCTION TESTS PASSED!")
            print("Luna AI is ready for production deployment! 🚀")
            return True
        else:
            print("\n❌ SOME TESTS FAILED!")
            print("Please check the test output above for details.")
            return False

    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Test runner error: {e}")
        return False
    finally:
        if server_process:
            stop_server(server_process)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
