#!/usr/bin/env python3
"""
Script to examine the structure of user-provided CSV files
"""

import csv
import os
import sys

def examine_csv(csv_path):
    """Examine CSV structure and show sample data"""
    print(f"📁 Examining: {csv_path}")
    print("=" * 50)
    
    if not os.path.exists(csv_path):
        print(f"❌ File not found: {csv_path}")
        return False
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as file:
            file.seek(0, 2)  # Seek to end
            file_size = file.tell()
            file.seek(0)  # Seek back to beginning
            
            print(f"📊 File size: {file_size:,} bytes")
            
            reader = csv.DictReader(file)
            
            print(f"📋 Columns: {list(reader.fieldnames)}")
            print(f"📋 Column count: {len(reader.fieldnames)}")
            
            print("\n📝 Sample data (first 5 rows):")
            for i, row in enumerate(reader):
                if i >= 5:
                    break
                print(f"Row {i+1}:")
                for key, value in row.items():
                    display_value = value[:100] + "..." if len(str(value)) > 100 else value
                    print(f"  {key}: {display_value}")
                print()
            
            file.seek(0)
            reader = csv.DictReader(file)
            row_count = sum(1 for row in reader)
            print(f"📊 Total rows: {row_count:,}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error reading CSV: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python examine_csv.py <csv_file_path>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    examine_csv(csv_path)
