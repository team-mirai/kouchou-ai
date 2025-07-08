#!/usr/bin/env python3
"""
Test education report creation after server issues were resolved
"""

import sys
import os
import json
sys.path.append('.')

from intelligent_report_automation import create_single_report_with_wait

def find_education_csv():
    """Find the education CSV file in attachments"""
    attachment_dirs = [
        "/home/ubuntu/attachments/7cff05f1-3057-49a5-a1c6-21556e40f588/_prs.csv",  # エネルギー
        "/home/ubuntu/attachments/33cbf471-f3ba-447f-9e0d-4d4ed210fd63/_prs.csv",  # システム
        "/home/ubuntu/attachments/a020bee5-709d-4712-abca-5cdadec567f2/_prs.csv",  # 経済財政
        "/home/ubuntu/attachments/b33566b6-830d-4841-ae7f-5766652fe794/_prs.csv",  # デジタル民主主義
        "/home/ubuntu/attachments/30fe0062-1e06-4faa-b04d-3a7f3363822e/_prs.csv",  # ビジョン
        "/home/ubuntu/attachments/69073cbe-fca1-44a0-aa06-1f042d7b3a23/_prs.csv",  # 医療
        "/home/ubuntu/attachments/48d47a45-98c8-4194-a281-d38d3842b226/_prs.csv",  # 科学技術
        "/home/ubuntu/attachments/1b3f6cb3-5dc5-4000-9695-2507513aac49/_prs.csv",  # 教育
        "/home/ubuntu/attachments/54ef645c-3df3-4473-8dd6-1b445655488a/_prs.csv",  # 行政改革
        "/home/ubuntu/attachments/737ea70e-92d3-4163-bd92-c862ce81df54/_prs.csv",  # 産業政策
        "/home/ubuntu/attachments/2a6697cb-a275-44e8-b877-fc9313f6bc93/_prs.csv",  # 子育て
        "/home/ubuntu/attachments/34c20c5e-7fcd-4636-a9ac-685dd7678bf3/_prs.csv",  # その他
        "/home/ubuntu/attachments/050ad88b-9762-452f-91e9-1366e0e2b90c/_prs.csv",  # 福祉
    ]
    
    education_csv = "/home/ubuntu/attachments/1b3f6cb3-5dc5-4000-9695-2507513aac49/_prs.csv"
    
    if os.path.exists(education_csv):
        return education_csv
    else:
        print(f"❌ Education CSV not found at: {education_csv}")
        return None

def test_education_report():
    """Test education report creation"""
    print("🎓 Testing Education Report Creation")
    print("=" * 60)
    
    education_csv = find_education_csv()
    if not education_csv:
        return False
    
    print(f"📄 Using education CSV: {education_csv}")
    
    config = {
        "reports": [{
            "input": "教育関連政策提案プルリクエスト分析7/8時点",
            "question": "教育関連政策提案プルリクエスト分析7/8時点",
            "intro": "7/8時点の教育関連政策提案プルリクエストを分析しました。",
            "csv_file_path": education_csv,
            "cluster": [12, 144],
            "provider": "openai",
            "model": "gpt-4o-mini",
            "workers": 1,
            "is_pubcom": False,
            "is_embedded_at_local": False,
            "enable_source_link": True
        }]
    }
    
    config_file = "education_report_config.json"
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    
    print(f"💾 Saved configuration: {config_file}")
    
    try:
        print(f"🔄 Creating education report with intelligent automation...")
        success = create_single_report_with_wait(config_file, 0)
        
        if success:
            print(f"✅ SUCCESS: Education report creation completed!")
            print(f"   Server issues appear to be resolved")
            return True
        else:
            print(f"❌ FAILED: Education report creation failed")
            print(f"   Server issues may still persist")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_education_report()
    sys.exit(0 if success else 1)
