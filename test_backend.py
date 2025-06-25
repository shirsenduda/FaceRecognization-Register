#!/usr/bin/env python3
"""
Test script to verify Flask backend is working correctly
Run this after starting your Flask server with: python app.py
"""

import requests
import json
import sys
from datetime import datetime

# Backend URL
BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api"

def test_endpoint(method, url, description, data=None, files=None):
    """Test a single endpoint"""
    print(f"\n🧪 Testing: {description}")
    print(f"   {method} {url}")
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, data=data, files=files, timeout=10)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.headers.get('content-type', '').startswith('application/json'):
            result = response.json()
            print(f"   Response: {json.dumps(result, indent=4)}")
        else:
            print(f"   Response: {response.text[:200]}...")
            
        return response.status_code == 200
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Connection Error: Backend server is not running!")
        print("   💡 Solution: Run 'python app.py' in another terminal first")
        return False
    except requests.exceptions.Timeout:
        print("   ❌ Timeout Error: Server took too long to respond")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    print("🚀 Face Recognition Backend Test Suite")
    print("=" * 50)
    print(f"📍 Testing backend at: {BASE_URL}")
    print(f"🕐 Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    tests = [
        ("GET", f"{BASE_URL}/", "Root endpoint (server info)"),
        ("GET", f"{BASE_URL}/test", "Test endpoint"),
        ("GET", f"{API_URL}/status", "API status endpoint"),
        ("GET", f"{API_URL}/stats", "Statistics endpoint"),
        ("GET", f"{API_URL}/registered_users", "Registered users endpoint"),
    ]
    
    passed = 0
    total = len(tests)
    
    for method, url, description in tests:
        if test_endpoint(method, url, description):
            passed += 1
            print("   ✅ PASSED")
        else:
            print("   ❌ FAILED")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Backend is working correctly.")
        print("💡 You can now use the frontend interface.")
    else:
        print("⚠️ Some tests failed. Please check the backend server.")
        
        if passed == 0:
            print("\n🔧 Troubleshooting steps:")
            print("1. Make sure Flask backend is running:")
            print("   python app.py")
            print("2. Check if port 5000 is available:")
            print("   netstat -an | grep 5000")
            print("3. Install required dependencies:")
            print("   pip install flask flask-cors")
            print("4. Check firewall settings")
    
    print("=" * 50)

if __name__ == "__main__":
    main()