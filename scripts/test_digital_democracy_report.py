#!/usr/bin/env python3
"""
Test Digital Democracy report creation via API since user reported manual success
"""

import sys
import os
import json
sys.path.append('.')

from intelligent_report_automation import create_single_report_with_wait

def find_digital_democracy_csv():
    """Find the Digital Democracy CSV file in attachments"""
    digital_democracy_csv = "/home/ubuntu/attachments/b33566b6-830d-4841-ae7f-5766652fe794/_prs.csv"
    
    if os.path.exists(digital_democracy_csv):
        return digital_democracy_csv
    else:
        print(f"❌ Digital Democracy CSV not found at: {digital_democracy_csv}")
        return None

def test_digital_democracy_report():
    """Test Digital Democracy report creation via API"""
    print("🏛️ Testing Digital Democracy Report Creation (API)")
    print("=" * 60)
    
    digital_democracy_csv = find_digital_democracy_csv()
    if not digital_democracy_csv:
        return False
    
    print(f"📄 Using Digital Democracy CSV: {digital_democracy_csv}")
    
    config = {
        "reports": [{
            "input": "デジタル民主主義関連政策提案プルリクエスト分析7/8時点",
            "question": "デジタル民主主義関連政策提案プルリクエスト分析7/8時点",
            "intro": "7/8時点のデジタル民主主義関連政策提案プルリクエストを分析しました。",
            "csv_file_path": digital_democracy_csv,
            "cluster": [12, 144],
            "provider": "openai",
            "model": "gpt-4o-mini",
            "workers": 1,
            "is_pubcom": False,
            "is_embedded_at_local": False,
            "enable_source_link": True
        }]
    }
    
    config_file = "digital_democracy_report_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved configuration: {config_file}")
    
    try:
        print(f"🔄 Creating Digital Democracy report with intelligent automation...")
        print(f"   (User reported manual success - testing API automation)")
        success = create_single_report_with_wait(config_file, 0)
        
        if success:
            print(f"✅ SUCCESS: Digital Democracy report creation completed via API!")
            print(f"   Server issues appear to be resolved for this report")
            print(f"   API automation is working correctly")
            return True
        else:
            print(f"❌ FAILED: Digital Democracy report creation failed via API")
            print(f"   Manual vs API methods may have different behavior")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_digital_democracy_report()
    
    if success:
        print(f"\n🎯 CONCLUSION: API automation is working for Digital Democracy")
        print(f"   Education report failure may be data-specific")
    else:
        print(f"\n🎯 CONCLUSION: API automation still has issues")
        print(f"   Manual vs API methods may differ")
    
    sys.exit(0 if success else 1)
