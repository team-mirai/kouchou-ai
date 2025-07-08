#!/usr/bin/env python3
"""
Script to create the second report with proper configuration
"""

import sys
import os
sys.path.append('.')

from automate_reports import load_report_configs, KouchouAIClient, validate_environment

def create_second_report():
    """Create the second report using マイナンバーカード CSV data"""
    print("🚀 Creating Second Report")
    print("=" * 50)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        print(f"✅ Environment validated")
        print(f"   API URL: {api_base_url}")
        print(f"   API Key: {admin_api_key[:8]}...")
        
        client = KouchouAIClient(api_base_url, admin_api_key)
        print(f"✅ Client initialized")
        
        configs = load_report_configs('second_report_config.json')
        print(f"✅ Configuration loaded: {len(configs)} report(s)")
        
        config = configs[0]
        print(f"\n📊 Creating second report:")
        print(f"   ID: {config.input}")
        print(f"   Question: {config.question}")
        print(f"   CSV: {config.csv_file_path}")
        print(f"   Cluster: {config.cluster}")
        
        success = client.create_report(config)
        
        if success:
            print(f"\n🎉 SUCCESS: Second report '{config.input}' created successfully!")
            print(f"   ✅ Report processing started with マイナンバーカード data")
            print(f"   🔗 Check admin interface: https://client-admin.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io/")
            print(f"   📊 Data: 30,084 entries processed")
            return True
        else:
            print(f"\n❌ FAILED: Second report '{config.input}' creation failed.")
            return False
            
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = create_second_report()
    sys.exit(0 if success else 1)
