#!/usr/bin/env python3
"""
Test report creation with a different CSV file to isolate if the issue
is specific to the economic CSV data or a general server problem
"""

import sys
import os
sys.path.append('.')

from intelligent_report_automation import create_single_report_with_wait

def test_different_csv_files():
    """Test with different CSV files to isolate the issue"""
    print("🧪 Testing Different CSV Files")
    print("=" * 60)
    
    print("📋 Test 1: Using Energy CSV (previously successful)")
    
    energy_csv = "/home/ubuntu/attachments/7cff05f1-3057-49a5-a1c6-21556e40f588/_prs.csv"
    
    if os.path.exists(energy_csv):
        print(f"   ✅ Energy CSV exists: {energy_csv}")
        
        import json
        test_config = {
            "reports": [{
                "input": "エネルギー関連政策提案プルリクエスト分析7/8時点（再テスト）",
                "question": "エネルギー関連政策提案プルリクエスト分析7/8時点（再テスト）",
                "intro": "7/8時点のエネルギー関連政策提案プルリクエスト再テスト分析です。",
                "csv_file_path": energy_csv,
                "cluster": [12, 144],
                "provider": "openai",
                "model": "gpt-4o-mini",
                "workers": 1,
                "is_pubcom": False,
                "is_embedded_at_local": False,
                "enable_source_link": True
            }]
        }
        
        with open("test_energy_rerun.json", 'w', encoding='utf-8') as f:
            json.dump(test_config, f, ensure_ascii=False, indent=2)
        
        print(f"   🔄 Testing energy CSV with current system...")
        success = create_single_report_with_wait("test_energy_rerun.json", 0)
        
        if success:
            print(f"   ✅ Energy CSV test PASSED - server is working")
            print(f"   💡 This suggests the issue is specific to economic CSV data")
            return True
        else:
            print(f"   ❌ Energy CSV test FAILED - server issue or system problem")
            print(f"   💡 This suggests a broader server or system issue")
            return False
    else:
        print(f"   ❌ Energy CSV not found: {energy_csv}")
        return False

if __name__ == "__main__":
    success = test_different_csv_files()
    
    if success:
        print(f"\n🎯 CONCLUSION: Issue is specific to economic CSV data")
        print(f"   Recommended: Examine economic CSV content for problematic data")
    else:
        print(f"\n🎯 CONCLUSION: Broader server or system issue")
        print(f"   Recommended: Check server logs or contact system administrator")
    
    sys.exit(0 if success else 1)
