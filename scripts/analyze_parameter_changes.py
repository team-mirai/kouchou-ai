#!/usr/bin/env python3
"""
Analyze parameter changes between working and broken API states
"""

import sys
import json
sys.path.append('.')

def analyze_parameter_changes():
    """Analyze parameter changes that could cause API failures"""
    print("🔍 Parameter Change Analysis")
    print("=" * 60)
    
    print("📋 Key Findings from Git History:")
    print("  1. Commit a46b59e: 'is_pubcomを常にTrueにする' (Always set is_pubcom to True)")
    print("     - Server schema changed: is_pubcom default from False to True")
    print("     - Client UI removed is_pubcom checkbox")
    print("     - Manual interface now always sends is_pubcom=True")
    
    print("  2. Commit 055baed: 'implement source url feature'")
    print("     - Added enable_source_link parameter")
    print("     - May have changed comment processing logic")
    
    print("\n🔧 Current Automation Script Payload:")
    print("  - is_pubcom: False (hardcoded in automation)")
    print("  - enable_source_link: True (correctly set)")
    
    print("\n🎯 Expected Server Behavior:")
    print("  - Server schema expects is_pubcom=True by default")
    print("  - Manual interface always sends is_pubcom=True")
    print("  - API automation sends is_pubcom=False (mismatch!)")
    
    print("\n💡 Root Cause Analysis:")
    print("  1. Parameter Mismatch: Automation sends is_pubcom=False, server expects True")
    print("  2. Processing Logic: Server may have changed CSV processing for is_pubcom=False")
    print("  3. Feature Regression: Source URL feature may conflict with is_pubcom=False")
    
    print("\n🚨 Critical Parameter Differences:")
    print("  Manual (Working):")
    print("    - is_pubcom: true (always)")
    print("    - enable_source_link: varies")
    print("  ")
    print("  API Automation (Failing):")
    print("    - is_pubcom: false (hardcoded)")
    print("    - enable_source_link: true")
    
    print("\n📊 Recommended Investigation:")
    print("  1. Test API with is_pubcom=True to match manual interface")
    print("  2. Check if server processing changed for is_pubcom=False mode")
    print("  3. Verify source URL feature compatibility with CSV modes")
    
    return True

if __name__ == "__main__":
    success = analyze_parameter_changes()
    sys.exit(0 if success else 1)
