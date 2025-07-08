#!/usr/bin/env python3
"""
Comprehensive diagnostic tool for ADMIN_API_KEY setup issues
Identifies all possible causes why API key validation fails locally
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_environment_sources():
    """Check all possible sources of environment variables"""
    print("🔍 Environment Variable Sources Analysis")
    print("=" * 60)
    
    results = {}
    
    env_key = os.getenv("ADMIN_API_KEY")
    results['direct_env'] = env_key
    print(f"1. Direct os.getenv(): '{env_key}'")
    
    try:
        result = subprocess.run(['printenv', 'ADMIN_API_KEY'], 
                              capture_output=True, text=True)
        shell_value = result.stdout.strip() if result.returncode == 0 else None
        results['shell_env'] = shell_value
        print(f"2. Shell printenv: '{shell_value}'")
    except Exception as e:
        results['shell_env'] = f"Error: {e}"
        print(f"2. Shell printenv: Error - {e}")
    
    env_file = Path(".env")
    if env_file.exists():
        try:
            with open(env_file, 'r') as f:
                content = f.read()
                env_lines = [line for line in content.split('\n') 
                           if line.startswith('ADMIN_API_KEY')]
                results['env_file'] = env_lines
                print(f"3. .env file: {env_lines}")
        except Exception as e:
            results['env_file'] = f"Error: {e}"
            print(f"3. .env file: Error - {e}")
    else:
        results['env_file'] = "Not found"
        print(f"3. .env file: Not found")
    
    current_dir = Path.cwd()
    for parent in [current_dir.parent, current_dir.parent.parent]:
        env_file = parent / ".env"
        if env_file.exists():
            try:
                with open(env_file, 'r') as f:
                    content = f.read()
                    env_lines = [line for line in content.split('\n') 
                               if line.startswith('ADMIN_API_KEY')]
                    if env_lines:
                        results[f'env_file_{parent.name}'] = env_lines
                        print(f"4. .env in {parent}: {env_lines}")
            except Exception as e:
                print(f"4. .env in {parent}: Error - {e}")
    
    env_example = Path(".env.example")
    if env_example.exists():
        try:
            with open(env_example, 'r') as f:
                content = f.read()
                env_lines = [line for line in content.split('\n') 
                           if line.startswith('ADMIN_API_KEY')]
                results['env_example'] = env_lines
                print(f"5. .env.example: {env_lines}")
        except Exception as e:
            results['env_example'] = f"Error: {e}"
            print(f"5. .env.example: Error - {e}")
    else:
        results['env_example'] = "Not found"
        print(f"5. .env.example: Not found")
    
    return results

def check_shell_environment():
    """Check shell-specific environment details"""
    print("\n🐚 Shell Environment Analysis")
    print("=" * 60)
    
    shell = os.getenv('SHELL', 'unknown')
    print(f"1. Current shell: {shell}")
    
    print(f"2. Platform: {platform.system()} {platform.release()}")
    print(f"3. Python version: {sys.version}")
    
    print(f"4. Working directory: {os.getcwd()}")
    
    venv = os.getenv('VIRTUAL_ENV')
    conda_env = os.getenv('CONDA_DEFAULT_ENV')
    print(f"5. Virtual env: {venv or 'None'}")
    print(f"6. Conda env: {conda_env or 'None'}")
    
    path_dirs = os.getenv('PATH', '').split(os.pathsep)
    print(f"7. PATH entries: {len(path_dirs)} directories")
    
    home = Path.home()
    config_files = [
        '.bashrc', '.bash_profile', '.zshrc', '.profile', 
        '.fish_config', '.config/fish/config.fish'
    ]
    
    print(f"8. Shell config files:")
    for config_file in config_files:
        config_path = home / config_file
        if config_path.exists():
            print(f"   ✅ {config_file}")
        else:
            print(f"   ❌ {config_file}")

def test_python_import_path():
    """Test Python import and path issues"""
    print("\n🐍 Python Import Analysis")
    print("=" * 60)
    
    print(f"1. Current working directory: {os.getcwd()}")
    print(f"2. Python path entries:")
    for i, path in enumerate(sys.path):
        print(f"   {i}: {path}")
    
    try:
        sys.path.append('.')
        from automate_reports import validate_environment
        print(f"3. ✅ automate_reports import successful")
        
        try:
            api_url, api_key = validate_environment()
            print(f"4. ✅ validate_environment() successful")
            print(f"   API URL: {api_url}")
            print(f"   API Key: {api_key[:8] if api_key else 'None'}...")
        except Exception as e:
            print(f"4. ❌ validate_environment() failed: {e}")
            
    except ImportError as e:
        print(f"3. ❌ automate_reports import failed: {e}")
        print(f"   Make sure you're in the scripts/ directory")

def test_different_api_keys():
    """Test with different API key values"""
    print("\n🔑 API Key Testing")
    print("=" * 60)
    
    test_keys = [
        ("Production", "QJR5RJpfEZTv1"),
        ("Local Development", "admin"),
        ("Empty String", ""),
        ("None", None)
    ]
    
    original_key = os.getenv("ADMIN_API_KEY")
    
    for name, key in test_keys:
        print(f"\n🧪 Testing {name} key...")
        
        if key is None:
            if "ADMIN_API_KEY" in os.environ:
                del os.environ["ADMIN_API_KEY"]
        else:
            os.environ["ADMIN_API_KEY"] = key
        
        try:
            sys.path.append('.')
            from automate_reports import validate_environment
            
            api_url, api_key = validate_environment()
            print(f"   ✅ Validation passed")
            print(f"   Key: {key[:8] if key else 'None'}...")
            
        except Exception as e:
            print(f"   ❌ Validation failed: {e}")
    
    if original_key:
        os.environ["ADMIN_API_KEY"] = original_key
    elif "ADMIN_API_KEY" in os.environ:
        del os.environ["ADMIN_API_KEY"]

def provide_solutions():
    """Provide comprehensive solutions"""
    print("\n💡 Comprehensive Solutions")
    print("=" * 60)
    
    print("🎯 MOST LIKELY SOLUTIONS:")
    print()
    print("1. 🔧 Set environment variable in current shell:")
    print("   export ADMIN_API_KEY='QJR5RJpfEZTv1'")
    print("   echo $ADMIN_API_KEY  # Verify it's set")
    print()
    
    print("2. 🗂️ Create .env file in scripts directory:")
    print("   cd /path/to/kouchou-ai/scripts")
    print("   echo 'ADMIN_API_KEY=QJR5RJpfEZTv1' > .env")
    print()
    
    print("3. 🐚 Add to shell profile (persistent):")
    print("   # For bash:")
    print("   echo 'export ADMIN_API_KEY=\"QJR5RJpfEZTv1\"' >> ~/.bashrc")
    print("   source ~/.bashrc")
    print()
    print("   # For zsh:")
    print("   echo 'export ADMIN_API_KEY=\"QJR5RJpfEZTv1\"' >> ~/.zshrc")
    print("   source ~/.zshrc")
    print()
    
    print("4. 🔍 Verify setup:")
    print("   echo $ADMIN_API_KEY")
    print("   python -c \"import os; print(os.getenv('ADMIN_API_KEY'))\"")
    print("   python test_api_key_validation.py")
    print()
    
    print("🚨 COMMON ISSUES:")
    print()
    print("• Wrong directory: Make sure you're in scripts/ directory")
    print("• Shell session: Environment variables only persist in current session")
    print("• Typos: Check for spaces, quotes, or case sensitivity")
    print("• Virtual environments: May need to set in activated environment")
    print("• IDE/Editor: May need to restart IDE after setting environment variables")

def main():
    """Main diagnostic function"""
    print("🚨 COMPREHENSIVE ADMIN_API_KEY DIAGNOSTIC TOOL")
    print("=" * 70)
    print("This tool will identify why API key validation fails locally")
    print()
    
    env_results = check_environment_sources()
    check_shell_environment()
    test_python_import_path()
    test_different_api_keys()
    provide_solutions()
    
    print("\n📋 DIAGNOSTIC SUMMARY")
    print("=" * 60)
    
    current_key = env_results.get('direct_env')
    if current_key:
        print(f"✅ ADMIN_API_KEY is set: {current_key[:8]}...")
        print("   If you're still getting errors, check import path or API connectivity")
    else:
        print("❌ ADMIN_API_KEY is NOT set")
        print("   This is the most likely cause of your error")
    
    print(f"\n🎯 RECOMMENDED ACTION:")
    if not current_key:
        print("   1. Run: export ADMIN_API_KEY='QJR5RJpfEZTv1'")
        print("   2. Verify: echo $ADMIN_API_KEY")
        print("   3. Test: python test_api_key_validation.py")
    else:
        print("   1. Check you're in the correct directory (scripts/)")
        print("   2. Verify network connectivity to API")
        print("   3. Check for import path issues")

if __name__ == "__main__":
    main()
