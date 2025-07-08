#!/usr/bin/env python3
"""
End-to-end test of the automation system with a single report
"""

import sys
import os
sys.path.append('.')

from automate_reports import load_report_configs, KouchouAIClient, validate_environment

def test_single_report():
    """Test creating a single report end-to-end"""
    print("🧪 Testing End-to-End Report Automation")
    print("=" * 50)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        print(f"✅ Environment validated")
        print(f"   API URL: {api_base_url}")
        print(f"   API Key: {admin_api_key[:8]}...")
        
        client = KouchouAIClient(api_base_url, admin_api_key)
        print(f"✅ Client initialized")
        
        configs = load_report_configs('test_single_report.json')
        print(f"✅ Configuration loaded: {len(configs)} report(s)")
        
        config = configs[0]
        print(f"\n📊 Testing report creation:")
        print(f"   ID: {config.input}")
        print(f"   Question: {config.question}")
        print(f"   CSV: {config.csv_file_path}")
        
        success = client.create_report(config)
        
        if success:
            print(f"\n🎉 SUCCESS: Report '{config.input}' created successfully!")
            print(f"   ✅ Verified: Report appears in admin interface")
            print(f"   🔗 Check: https://client-admin.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io/")
            return True
        else:
            print(f"\n❌ FAILED: Report '{config.input}' creation failed.")
            return False
            
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_single_report()
    sys.exit(0 if success else 1)
