#!/usr/bin/env python3
"""
Test script to help validate ADMIN_API_KEY setup
"""

import os
import sys
sys.path.append('.')

from automate_reports import validate_environment, KouchouAIClient

def test_api_key_validation():
    """Test API key validation and connection"""
    print("🔑 Testing ADMIN_API_KEY Validation")
    print("=" * 50)
    
    current_key = os.getenv("ADMIN_API_KEY")
    print(f"Current ADMIN_API_KEY: '{current_key}'")
    
    if not current_key:
        print("❌ ADMIN_API_KEY is not set!")
        print("\n💡 Solutions:")
        print("1. For local development:")
        print("   export ADMIN_API_KEY='admin'")
        print("\n2. For production environment:")
        print("   export ADMIN_API_KEY='QJR5RJpfEZTv1'")
        print("\n3. Check .env.example for reference values")
        return False
    
    try:
        api_url, api_key = validate_environment()
        print(f"✅ Environment validation successful!")
        print(f"   API URL: {api_url}")
        print(f"   API Key: {api_key[:8]}...")
        
        print(f"\n🌐 Testing API connection...")
        client = KouchouAIClient(api_url, api_key)
        
        response = client.session.get(
            f"{client.api_base_url}/admin/reports",
            headers={"x-api-key": client.admin_api_key},
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            reports = response.json()
            print(f"   ✅ API connection successful! Found {len(reports)} reports")
            return True
        elif response.status_code == 401:
            print(f"   ❌ Authentication failed - incorrect API key")
            print(f"   💡 Try: export ADMIN_API_KEY='QJR5RJpfEZTv1'")
            return False
        else:
            print(f"   ⚠️  Unexpected response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = test_api_key_validation()
    
    if success:
        print(f"\n🎉 All tests passed! You can now run the automation scripts.")
    else:
        print(f"\n🔧 Please fix the API key setup and try again.")
    
    sys.exit(0 if success else 1)
