#!/usr/bin/env python3
"""
Test the API key from environment variable
"""

import requests
import os

def test_correct_api_key():
    """Test the API key from environment variable"""
    api_key = os.getenv("ADMIN_API_KEY")
    url = "https://api.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io/admin/reports"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json={"test": "minimal"}, timeout=10)
        if not api_key:
            print("❌ ADMIN_API_KEY environment variable not set")
            return False
            
        print(f"API Key: {api_key[:8]}...")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        
        if response.status_code == 401:
            print("❌ API key still invalid")
            return False
        elif response.status_code in [200, 202, 422]:  # 422 might be validation error but auth worked
            print("✅ API key authentication successful!")
            return True
        else:
            print(f"⚠️ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API key: {e}")
        return False

if __name__ == "__main__":
    test_correct_api_key()
