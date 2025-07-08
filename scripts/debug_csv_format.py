#!/usr/bin/env python3
"""
Debug script to check CSV format and content
"""

import csv
import sys

def debug_csv_file(csv_path):
    """Debug CSV file format and content"""
    print(f"🔍 Debugging CSV file: {csv_path}")
    print("=" * 60)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            print("📄 First 3 lines:")
            for i, line in enumerate(f):
                if i >= 3:
                    break
                print(f"  {i+1}: {line.strip()[:100]}...")
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            print(f"\n📊 CSV Structure:")
            print(f"  Columns: {reader.fieldnames}")
            
            rows = list(reader)
            print(f"  Total rows: {len(rows)}")
            
            if rows:
                print(f"\n📝 Sample row:")
                sample = rows[0]
                for key, value in sample.items():
                    print(f"  {key}: {value[:100] if value else 'None'}...")
                
                required_fields = ['text', 'url']
                missing_fields = [field for field in required_fields if field not in reader.fieldnames]
                if missing_fields:
                    print(f"\n❌ Missing required fields: {missing_fields}")
                else:
                    print(f"\n✅ All required fields present")
                
                empty_text = sum(1 for row in rows if not row.get('text', '').strip())
                empty_url = sum(1 for row in rows if not row.get('url', '').strip())
                
                print(f"\n📈 Data Quality:")
                print(f"  Empty text fields: {empty_text}/{len(rows)}")
                print(f"  Empty URL fields: {empty_url}/{len(rows)}")
                
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")

if __name__ == "__main__":
    csv_path = "/home/ubuntu/attachments/a020bee5-709d-4712-abca-5cdadec567f2/_prs.csv"
    debug_csv_file(csv_path)
