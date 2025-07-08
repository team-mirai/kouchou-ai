#!/usr/bin/env python3
"""
Script to identify and map all CSV files from user attachments
"""

import os
import glob

def identify_csv_files():
    """Identify all CSV files and their directory mappings"""
    print("📁 Identifying all CSV files from user attachments")
    print("=" * 60)
    
    attachment_dirs = glob.glob("/home/ubuntu/attachments/*/")
    
    csv_files = []
    for i, dir_path in enumerate(sorted(attachment_dirs)):
        csv_path = os.path.join(dir_path, "_prs.csv")
        if os.path.exists(csv_path):
            file_size = os.path.getsize(csv_path)
            csv_files.append({
                "index": i + 1,
                "directory": os.path.basename(dir_path.rstrip('/')),
                "path": csv_path,
                "size": file_size
            })
    
    print(f"Found {len(csv_files)} CSV files:")
    print()
    
    for csv_file in csv_files:
        print(f"File {csv_file['index']}:")
        print(f"  Directory: {csv_file['directory']}")
        print(f"  Path: {csv_file['path']}")
        print(f"  Size: {csv_file['size']:,} bytes")
        print()
    
    used_file = "/home/ubuntu/attachments/7cff05f1-3057-49a5-a1c6-21556e40f588/_prs.csv"
    for csv_file in csv_files:
        if csv_file['path'] == used_file:
            print(f"🎯 USED FILE: File {csv_file['index']} (Directory: {csv_file['directory']})")
            print(f"   This was the file processed in the first report")
            break
    
    return csv_files

if __name__ == "__main__":
    identify_csv_files()
