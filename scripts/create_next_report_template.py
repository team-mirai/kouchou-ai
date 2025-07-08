#!/usr/bin/env python3
"""
Template generator for creating descriptive report configurations
"""

import json
from datetime import datetime

def create_report_template(csv_file_path, topic, file_number, total_files):
    """Create a report configuration with descriptive title and date"""
    
    current_date = datetime.now().strftime("%-m/%-d")
    
    report_id = f"{topic.lower().replace(' ', '-')}-pr-analysis-{current_date.replace('/', '-')}"
    title = f"{topic}関連政策提案プルリクエスト分析{current_date}時点"
    
    config = {
        "input": report_id,
        "question": title,
        "intro": f"GitHub上の{topic}関連政策提案プルリクエストを分析し、主要なテーマや傾向を把握します。{topic}分野における市民からの提案内容を整理・分類します。",
        "csv_file_path": csv_file_path,
        "cluster": [5, 25],
        "provider": "openai",
        "model": "gpt-4o-mini",
        "workers": 1,
        "is_pubcom": False,
        "is_embedded_at_local": False,
        "enable_source_link": True
    }
    
    return config

def main():
    """Example usage"""
    print("📝 Report Template Generator")
    print("=" * 40)
    
    topics = ["エネルギー", "外交", "教育", "医療", "経済"]
    
    for i, topic in enumerate(topics):
        config = create_report_template(
            f"/home/ubuntu/attachments/example-{i+1}/_prs.csv",
            topic,
            i + 1,
            len(topics)
        )
        print(f"\n{topic}レポート設定例:")
        print(f"  ID: {config['input']}")
        print(f"  Title: {config['question']}")

if __name__ == "__main__":
    main()
