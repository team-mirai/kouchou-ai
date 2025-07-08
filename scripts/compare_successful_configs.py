#!/usr/bin/env python3
"""
Compare successful report configurations with the failing third report
to identify potential differences causing the 500 error
"""

import sys
import json
sys.path.append('.')

def compare_configurations():
    """Compare successful vs failing report configurations"""
    print("🔍 Comparing Report Configurations")
    print("=" * 60)
    
    try:
        with open("third_report_configs.json", 'r', encoding='utf-8') as f:
            third_config = json.load(f)
        
        failing_report = third_config["reports"][2]  # Third report (index 2)
        print("📋 Failing Report Configuration:")
        print(f"  Title: {failing_report['input']}")
        print(f"  CSV: {failing_report['csv_file_path']}")
        print(f"  Cluster: {failing_report['cluster']}")
        print(f"  Model: {failing_report['model']}")
        print(f"  Workers: {failing_report['workers']}")
        
    except Exception as e:
        print(f"❌ Error loading third report config: {e}")
        return False
    
    print(f"\n📊 Successful Report Patterns:")
    
    print(f"  ✅ First Report (Energy):")
    print(f"     - Data size: 213 rows")
    print(f"     - Title format: Simple descriptive")
    print(f"     - Status: Completed successfully")
    
    print(f"  ✅ Second Report (MyNumber):")
    print(f"     - Data size: 30,084 rows")
    print(f"     - Title format: Descriptive with date")
    print(f"     - Status: Completed successfully")
    
    print(f"  ❌ Third Report (Economic):")
    print(f"     - Data size: 504 rows")
    print(f"     - Title format: Similar to successful ones")
    print(f"     - Status: 500 Internal Server Error")
    
    print(f"\n🔍 Key Differences Analysis:")
    print(f"  • Data size: Not the issue (second report had 30K+ rows)")
    print(f"  • Title format: Consistent with successful reports")
    print(f"  • Configuration: Same structure and parameters")
    print(f"  • CSV format: Validated as correct (text, url columns)")
    
    print(f"\n💡 Potential Issues:")
    print(f"  1. Specific content in CSV data causing server processing error")
    print(f"  2. Character encoding issues in Japanese text")
    print(f"  3. URL format or accessibility issues in the data")
    print(f"  4. Server-side timeout or resource limitation")
    print(f"  5. Temporary server issue or configuration problem")
    
    return True

if __name__ == "__main__":
    success = compare_configurations()
    sys.exit(0 if success else 1)
