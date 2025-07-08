#!/usr/bin/env python3
"""
Test with a smaller subset of the CSV data to see if size is the issue
"""

import sys
import os
import csv
import json
sys.path.append('.')

from automate_reports import KouchouAIClient, ReportConfig, validate_environment

def create_small_test_csv(original_csv, output_csv, max_rows=50):
    """Create a smaller test CSV with limited rows"""
    with open(original_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        
        with open(output_csv, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
            writer.writeheader()
            
            for i, row in enumerate(reader):
                if i >= max_rows:
                    break
                writer.writerow(row)
    
    print(f"Created test CSV with {max_rows} rows: {output_csv}")

def test_small_batch():
    """Test report creation with smaller data batch"""
    print("🧪 Testing Third Report with Smaller Data Batch")
    print("=" * 60)
    
    original_csv = "/home/ubuntu/attachments/a020bee5-709d-4712-abca-5cdadec567f2/_prs.csv"
    test_csv = "/home/ubuntu/repos/kouchou-ai/scripts/test_economic_small.csv"
    
    create_small_test_csv(original_csv, test_csv, max_rows=50)
    
    config = ReportConfig(
        input="経済財政関連政策提案プルリクエスト分析7/8時点（テスト50件）",
        question="経済財政関連政策提案プルリクエスト分析7/8時点（テスト50件）",
        intro="7/8時点の経済財政関連政策提案プルリクエスト50件のテスト分析です。",
        csv_file_path=test_csv,
        cluster=[12, 144],
        provider="openai",
        model="gpt-4o-mini",
        workers=1,
        is_pubcom=False,
        is_embedded_at_local=False,
        enable_source_link=True
    )
    
    try:
        api_url, api_key = validate_environment()
        client = KouchouAIClient(api_url, api_key)
        
        print(f"🔄 Creating test report with 50 rows...")
        success = client.create_report(config)
        
        if success:
            print(f"✅ SUCCESS: Small batch test passed!")
            print(f"   This suggests the issue may be related to data size")
            return True
        else:
            print(f"❌ FAILED: Small batch test also failed")
            print(f"   This suggests a different issue than data size")
            return False
            
    except Exception as e:
        print(f"💥 ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_small_batch()
    sys.exit(0 if success else 1)
