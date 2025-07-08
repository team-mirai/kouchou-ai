#!/usr/bin/env python3
"""
Intelligent report automation script that uses API status checking
instead of fixed time intervals to determine when to create the next report.
"""

import sys
import os
import time
import json
from typing import List, Dict, Any
sys.path.append('.')

from automate_reports import KouchouAIClient, ReportConfig, validate_environment

def check_processing_reports(client: KouchouAIClient) -> List[Dict[str, Any]]:
    """
    Check for currently processing reports via admin API
    
    Returns:
        List of processing reports (empty if none are processing)
    """
    try:
        response = client.session.get(
            f"{client.api_base_url}/admin/reports",
            headers={"x-api-key": client.admin_api_key}
        )
        
        if response.status_code != 200:
            print(f"⚠️  Failed to get reports status: HTTP {response.status_code}")
            return []
        
        reports = response.json()
        
        processing_reports = [
            report for report in reports 
            if report.get("status") == "processing"
        ]
        
        return processing_reports
        
    except Exception as e:
        print(f"❌ Error checking report status: {e}")
        return []

def wait_for_processing_completion(client: KouchouAIClient, max_wait_minutes: int = 60) -> bool:
    """
    Wait for all currently processing reports to complete
    
    Args:
        client: KouchouAI API client
        max_wait_minutes: Maximum time to wait in minutes
        
    Returns:
        True if all reports completed, False if timeout
    """
    start_time = time.time()
    max_wait_seconds = max_wait_minutes * 60
    
    print(f"🔍 Checking for processing reports...")
    
    while True:
        processing_reports = check_processing_reports(client)
        
        if not processing_reports:
            print("✅ No reports currently processing - ready to create next report")
            return True
        
        report_names = [report.get("slug", "unknown") for report in processing_reports]
        print(f"⏳ {len(processing_reports)} report(s) still processing: {', '.join(report_names)}")
        
        elapsed = time.time() - start_time
        if elapsed > max_wait_seconds:
            print(f"⏰ Timeout reached ({max_wait_minutes} minutes) - proceeding anyway")
            return False
        
        print(f"   Waiting 30 seconds before next check... ({elapsed/60:.1f}/{max_wait_minutes} min)")
        time.sleep(30)

def create_reports_intelligently(config_file: str = "report_configs.json") -> bool:
    """
    Create reports with intelligent waiting based on API status
    
    Args:
        config_file: Path to report configuration file
        
    Returns:
        True if all reports were created successfully
    """
    print("🚀 Starting Intelligent Report Automation")
    print("=" * 60)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        print(f"✅ Environment validated")
        print(f"   API URL: {api_base_url}")
        print(f"   API Key: {admin_api_key[:8]}...")
        
        client = KouchouAIClient(api_base_url, admin_api_key)
        print(f"✅ Client initialized")
        
        from automate_reports import load_report_configs
        configs = load_report_configs(config_file)
        print(f"✅ Configuration loaded: {len(configs)} report(s)")
        
        success_count = 0
        
        for i, config in enumerate(configs):
            print(f"\n📊 Processing Report {i+1}/{len(configs)}")
            print(f"   ID: {config.input}")
            print(f"   Question: {config.question}")
            print(f"   CSV: {config.csv_file_path}")
            
            if i > 0:  # Skip waiting for the first report
                print(f"\n⏳ Waiting for previous reports to complete...")
                completed = wait_for_processing_completion(client, max_wait_minutes=60)
                if not completed:
                    print(f"⚠️  Proceeding despite timeout - some reports may still be processing")
            
            print(f"\n🔄 Creating report: {config.input}")
            success = client.create_report(config)
            
            if success:
                print(f"✅ SUCCESS: Report '{config.input}' created successfully!")
                success_count += 1
            else:
                print(f"❌ FAILED: Report '{config.input}' creation failed.")
        
        print(f"\n🎉 Automation Complete!")
        print(f"   ✅ Successfully created: {success_count}/{len(configs)} reports")
        print(f"   ❌ Failed: {len(configs) - success_count}/{len(configs)} reports")
        
        if success_count == len(configs):
            print(f"   🔗 Check admin interface for processing status")
            return True
        else:
            print(f"   ⚠️  Some reports failed - check logs above for details")
            return False
            
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        return False

def create_single_report_with_wait(config_file: str, report_index: int = 0) -> bool:
    """
    Create a single report with intelligent waiting
    
    Args:
        config_file: Path to report configuration file
        report_index: Index of report to create (0-based)
        
    Returns:
        True if report was created successfully
    """
    print("🚀 Creating Single Report with Intelligent Waiting")
    print("=" * 60)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        client = KouchouAIClient(api_base_url, admin_api_key)
        
        from automate_reports import load_report_configs
        configs = load_report_configs(config_file)
        
        if report_index >= len(configs):
            print(f"❌ Invalid report index {report_index}. Available: 0-{len(configs)-1}")
            return False
        
        config = configs[report_index]
        
        print(f"📊 Target Report:")
        print(f"   ID: {config.input}")
        print(f"   Question: {config.question}")
        
        print(f"\n⏳ Checking for processing reports...")
        completed = wait_for_processing_completion(client, max_wait_minutes=60)
        
        if not completed:
            print(f"⚠️  Proceeding despite timeout")
        
        print(f"\n🔄 Creating report: {config.input}")
        success = client.create_report(config)
        
        if success:
            print(f"✅ SUCCESS: Report '{config.input}' created successfully!")
            return True
        else:
            print(f"❌ FAILED: Report '{config.input}' creation failed.")
            return False
            
    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "single":
            config_file = sys.argv[2] if len(sys.argv) > 2 else "report_configs.json"
            report_index = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            success = create_single_report_with_wait(config_file, report_index)
        else:
            success = create_reports_intelligently(sys.argv[1])
    else:
        success = create_reports_intelligently()
    
    sys.exit(0 if success else 1)
