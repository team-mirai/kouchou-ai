#!/usr/bin/env python3
"""
Simple script to test API key authentication
"""

import requests
import os

def test_api_key(api_key):
    """Test if an API key works with the admin endpoint"""
    url = "https://api.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io/admin/reports"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, headers=headers, json={"test": "data"}, timeout=10)
        print(f"API Key: {api_key}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:200]}...")
        return response.status_code != 401
    except Exception as e:
        print(f"Error testing API key {api_key}: {e}")
        return False

if __name__ == "__main__":
    test_keys = [
        "admin",  # Default from .env.example
        os.getenv("PASSWORD", ""),  # The password we have
        os.getenv("USERNAME", ""),  # Try username too
    ]
    
    for key in test_keys:
        if key:
            print(f"\nTesting API key: {key}")
            if test_api_key(key):
                print(f"✅ API key '{key}' works!")
                break
            else:
                print(f"❌ API key '{key}' failed")
        else:
            print("Skipping empty key")
