#!/usr/bin/env python3
"""
Test script for creating the third report using intelligent automation
"""

import sys
import os
sys.path.append('.')

from intelligent_report_automation import create_single_report_with_wait

def main():
    """Test the third report creation"""
    print("🚀 Testing Third Report Creation")
    print("=" * 50)
    
    config_file = "third_report_configs.json"
    report_index = 2  # Third report (zero-based index)
    
    print(f"Configuration file: {config_file}")
    print(f"Report index: {report_index}")
    print(f"Expected report: 経済財政関連政策提案プルリクエスト分析7/7時点")
    
    success = create_single_report_with_wait(config_file, report_index)
    
    if success:
        print(f"\n✅ Third report creation test PASSED!")
        print(f"Check the admin interface for processing status.")
    else:
        print(f"\n❌ Third report creation test FAILED!")
        print(f"Check the error messages above for details.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
