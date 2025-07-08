#!/usr/bin/env python3
"""
Test the is_pubcom parameter hypothesis - compare API calls with is_pubcom=False vs is_pubcom=True
to identify if this parameter change is causing the 500 Internal Server Error
"""

import sys
import os
import json
sys.path.append('.')

from intelligent_report_automation import create_single_report_with_wait

def test_is_pubcom_parameter():
    """Test both is_pubcom values to identify the parameter causing failures"""
    print("🧪 Testing is_pubcom Parameter Hypothesis")
    print("=" * 60)
    
    test_csv = "/home/ubuntu/attachments/7cff05f1-3057-49a5-a1c6-21556e40f588/_prs.csv"
    
    if not os.path.exists(test_csv):
        print(f"❌ Test CSV not found: {test_csv}")
        return False
    
    print(f"📄 Using test CSV: {test_csv}")
    
    print(f"\n🔍 Test 1: is_pubcom=False (current automation)")
    config_false = {
        "reports": [{
            "input": "test-is-pubcom-false",
            "question": "Test is_pubcom=False Parameter",
            "intro": "Testing is_pubcom=False parameter setting",
            "csv_file_path": test_csv,
            "cluster": [12, 144],
            "provider": "openai",
            "model": "gpt-4o-mini",
            "workers": 1,
            "is_pubcom": False,  # Current automation default
            "is_embedded_at_local": False,
            "enable_source_link": True
        }]
    }
    
    with open("test_is_pubcom_false.json", 'w', encoding='utf-8') as f:
        json.dump(config_false, f, ensure_ascii=False, indent=2)
    
    print(f"   🔄 Testing with is_pubcom=False...")
    success_false = create_single_report_with_wait("test_is_pubcom_false.json", 0)
    
    if success_false:
        print(f"   ✅ SUCCESS: is_pubcom=False works")
    else:
        print(f"   ❌ FAILED: is_pubcom=False fails (current behavior)")
    
    print(f"\n🔍 Test 2: is_pubcom=True (new server default)")
    config_true = {
        "reports": [{
            "input": "test-is-pubcom-true",
            "question": "Test is_pubcom=True Parameter",
            "intro": "Testing is_pubcom=True parameter setting",
            "csv_file_path": test_csv,
            "cluster": [12, 144],
            "provider": "openai",
            "model": "gpt-4o-mini",
            "workers": 1,
            "is_pubcom": True,  # New server default
            "is_embedded_at_local": False,
            "enable_source_link": True
        }]
    }
    
    with open("test_is_pubcom_true.json", 'w', encoding='utf-8') as f:
        json.dump(config_true, f, ensure_ascii=False, indent=2)
    
    print(f"   🔄 Testing with is_pubcom=True...")
    success_true = create_single_report_with_wait("test_is_pubcom_true.json", 0)
    
    if success_true:
        print(f"   ✅ SUCCESS: is_pubcom=True works")
    else:
        print(f"   ❌ FAILED: is_pubcom=True also fails")
    
    print(f"\n📊 Test Results Analysis:")
    print(f"  is_pubcom=False: {'✅ SUCCESS' if success_false else '❌ FAILED'}")
    print(f"  is_pubcom=True:  {'✅ SUCCESS' if success_true else '❌ FAILED'}")
    
    if success_true and not success_false:
        print(f"\n🎯 CONCLUSION: Parameter mismatch confirmed!")
        print(f"  - Server now requires is_pubcom=True")
        print(f"  - Automation script uses is_pubcom=False")
        print(f"  - This explains the API vs manual interface difference")
        return True
    elif success_false and not success_true:
        print(f"\n🎯 CONCLUSION: Parameter change not the issue")
        print(f"  - is_pubcom=False still works")
        print(f"  - Problem lies elsewhere")
        return False
    elif success_true and success_false:
        print(f"\n🎯 CONCLUSION: Both parameters work")
        print(f"  - is_pubcom parameter is not the issue")
        print(f"  - Server problem may be intermittent")
        return True
    else:
        print(f"\n🎯 CONCLUSION: Both parameters fail")
        print(f"  - Broader server issue beyond parameter changes")
        print(f"  - Need to investigate other causes")
        return False

if __name__ == "__main__":
    success = test_is_pubcom_parameter()
    sys.exit(0 if success else 1)
