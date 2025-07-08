#!/usr/bin/env python3
"""
Test script for intelligent report automation
"""

import sys
import os
sys.path.append('.')

from intelligent_report_automation import check_processing_reports, wait_for_processing_completion
from automate_reports import KouchouAIClient, validate_environment

def test_status_checking():
    """Test the report status checking functionality"""
    print("🧪 Testing Report Status Checking")
    print("=" * 50)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        client = KouchouAIClient(api_base_url, admin_api_key)
        
        print(f"✅ Client initialized")
        print(f"   API URL: {api_base_url}")
        print(f"   API Key: {admin_api_key[:8]}...")
        
        print(f"\n🔍 Testing report status retrieval...")
        processing_reports = check_processing_reports(client)
        
        print(f"📊 Current Status:")
        print(f"   Processing reports: {len(processing_reports)}")
        
        if processing_reports:
            print(f"   Reports currently processing:")
            for report in processing_reports:
                slug = report.get("slug", "unknown")
                status = report.get("status", "unknown")
                print(f"     - {slug}: {status}")
        else:
            print(f"   ✅ No reports currently processing")
        
        print(f"\n⏳ Testing wait functionality (5 second timeout)...")
        completed = wait_for_processing_completion(client, max_wait_minutes=0.083)  # ~5 seconds
        
        if completed:
            print(f"✅ Wait completed - no processing reports")
        else:
            print(f"⏰ Wait timed out - reports still processing")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_api_endpoints():
    """Test direct API endpoint access"""
    print("\n🧪 Testing Direct API Access")
    print("=" * 50)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        client = KouchouAIClient(api_base_url, admin_api_key)
        
        print(f"🔗 Testing GET /admin/reports")
        response = client.session.get(
            f"{client.api_base_url}/admin/reports",
            headers={"x-api-key": client.admin_api_key}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            reports = response.json()
            print(f"   ✅ Success: Retrieved {len(reports)} reports")
            
            for report in reports[:3]:  # Show first 3 reports
                slug = report.get("slug", "unknown")
                status = report.get("status", "unknown")
                title = report.get("title", "No title")[:50]
                print(f"     - {slug}: {status} | {title}...")
                
        else:
            print(f"   ❌ Failed: {response.text}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Intelligent Report Automation Tests")
    print("=" * 60)
    
    test1_success = test_status_checking()
    test2_success = test_api_endpoints()
    
    print(f"\n📋 Test Results:")
    print(f"   Status Checking: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"   API Endpoints: {'✅ PASS' if test2_success else '❌ FAIL'}")
    
    overall_success = test1_success and test2_success
    print(f"   Overall: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}")
    
    sys.exit(0 if overall_success else 1)
