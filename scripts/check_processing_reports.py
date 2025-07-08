#!/usr/bin/env python3
"""
Check for currently processing reports
"""

import sys
sys.path.append('.')

from intelligent_report_automation import check_processing_reports, KouchouAIClient
from automate_reports import validate_environment

def main():
    """Check processing reports"""
    print("🔍 Checking Currently Processing Reports")
    print("=" * 50)
    
    try:
        api_url, api_key = validate_environment()
        client = KouchouAIClient(api_url, api_key)
        processing = check_processing_reports(client)
        
        print(f"Currently processing reports: {len(processing)}")
        
        if processing:
            for report in processing:
                print(f"  - {report.get('slug', 'unknown')}: {report.get('status', 'unknown')}")
        else:
            print("  No reports currently processing")
            
        return len(processing) == 0
        
    except Exception as e:
        print(f"❌ Error checking reports: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
