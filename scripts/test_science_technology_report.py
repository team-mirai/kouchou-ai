#!/usr/bin/env python3
"""
Test Science and Technology report creation
"""

import sys
import os
import json
sys.path.append('.')

from intelligent_report_automation import create_single_report_with_wait

def find_science_technology_csv():
    """Find the Science and Technology CSV file in attachments"""
    potential_paths = [
        "/home/ubuntu/attachments/48d47a45-98c8-4194-a281-d38d3842b226/_prs.csv",  # 科学技術
    ]
    
    for csv_path in potential_paths:
        if os.path.exists(csv_path):
            return csv_path
    
    print(f"❌ Science and Technology CSV not found in expected locations")
    return None

def test_science_technology_report():
    """Test Science and Technology report creation"""
    print("🔬 Testing Science and Technology Report Creation")
    print("=" * 60)
    
    science_tech_csv = find_science_technology_csv()
    if not science_tech_csv:
        return False
    
    print(f"📄 Using Science and Technology CSV: {science_tech_csv}")
    
    try:
        with open(science_tech_csv, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            print(f"📊 CSV contains {len(lines)} lines")
    except Exception as e:
        print(f"⚠️ Could not read CSV: {e}")
    
    config = {
        "reports": [{
            "input": "科学技術関連政策提案プルリクエスト分析7/8時点",
            "question": "科学技術関連政策提案プルリクエスト分析7/8時点",
            "intro": "7/8時点の科学技術関連政策提案プルリクエストを分析しました。",
            "csv_file_path": science_tech_csv,
            "cluster": [12, 144],
            "provider": "openai",
            "model": "gpt-4o-mini",
            "workers": 1,
            "is_pubcom": False,
            "is_embedded_at_local": False,
            "enable_source_link": True
        }]
    }
    
    config_file = "science_technology_report_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved configuration: {config_file}")
    
    try:
        print(f"🔄 Creating Science and Technology report with intelligent automation...")
        success = create_single_report_with_wait(config_file, 0)
        
        if success:
            print(f"✅ SUCCESS: Science and Technology report creation completed!")
            print(f"   API automation is working for this CSV")
            return True
        else:
            print(f"❌ FAILED: Science and Technology report creation failed")
            print(f"   May be CSV-specific or server-side issue")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_science_technology_report()
    
    if success:
        print(f"\n🎯 CONCLUSION: Science and Technology CSV works with API automation")
        print(f"   Server issues may be resolved or CSV-specific")
    else:
        print(f"\n🎯 CONCLUSION: Science and Technology CSV still fails")
        print(f"   Broader server issue or data-specific problem")
    
    sys.exit(0 if success else 1)
