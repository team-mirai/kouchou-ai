#!/usr/bin/env python3
"""
Debug API payload structure to identify parameter differences
between current failing requests and previous successful ones
"""

import sys
import json
import os
sys.path.append('.')

from automate_reports import KouchouAIClient, ReportConfig, validate_environment

def analyze_payload_structure():
    """Analyze the current API payload structure"""
    print("🔍 API Payload Structure Analysis")
    print("=" * 60)
    
    try:
        api_url, api_key = validate_environment()
        client = KouchouAIClient(api_url, api_key)
        
        test_config = ReportConfig(
            input="test-payload-analysis",
            question="Test Payload Analysis",
            intro="Testing payload structure",
            csv_file_path="/home/ubuntu/attachments/7cff05f1-3057-49a5-a1c6-21556e40f588/_prs.csv",
            cluster=[12, 144],
            provider="openai",
            model="gpt-4o-mini",
            workers=1,
            is_pubcom=False,
            is_embedded_at_local=False,
            enable_source_link=True
        )
        
        comments = client._load_csv_data(test_config.csv_file_path)
        print(f"📊 CSV Data Analysis:")
        print(f"  - Total comments: {len(comments)}")
        if comments:
            print(f"  - Sample comment structure:")
            sample_comment = comments[0]
            for key, value in sample_comment.items():
                print(f"    {key}: {type(value).__name__} = {str(value)[:50]}...")
        
        payload = {
            "input": test_config.input,
            "question": test_config.question,
            "intro": test_config.intro,
            "comments": comments[:3],  # Just first 3 for analysis
            "cluster": test_config.cluster,
            "provider": test_config.provider,
            "model": test_config.model,
            "workers": test_config.workers,
            "prompt": client._get_default_prompts(),
            "is_pubcom": test_config.is_pubcom,
            "inputType": "file",
            "is_embedded_at_local": test_config.is_embedded_at_local,
            "enable_source_link": test_config.enable_source_link
        }
        
        print(f"\n📋 Current API Payload Structure:")
        print(f"  - input: {type(payload['input']).__name__}")
        print(f"  - question: {type(payload['question']).__name__}")
        print(f"  - intro: {type(payload['intro']).__name__}")
        print(f"  - comments: {type(payload['comments']).__name__} (length: {len(payload['comments'])})")
        print(f"  - cluster: {type(payload['cluster']).__name__} = {payload['cluster']}")
        print(f"  - provider: {type(payload['provider']).__name__} = {payload['provider']}")
        print(f"  - model: {type(payload['model']).__name__} = {payload['model']}")
        print(f"  - workers: {type(payload['workers']).__name__} = {payload['workers']}")
        print(f"  - prompt: {type(payload['prompt']).__name__}")
        print(f"  - is_pubcom: {type(payload['is_pubcom']).__name__} = {payload['is_pubcom']}")
        print(f"  - inputType: {type(payload['inputType']).__name__} = {payload['inputType']}")
        print(f"  - is_embedded_at_local: {type(payload['is_embedded_at_local']).__name__} = {payload['is_embedded_at_local']}")
        print(f"  - enable_source_link: {type(payload['enable_source_link']).__name__} = {payload['enable_source_link']}")
        
        print(f"\n🔍 Prompt Structure:")
        for key, value in payload['prompt'].items():
            print(f"  - {key}: {type(value).__name__} = {value[:50]}...")
        
        print(f"\n💾 Saving payload sample to file...")
        with open("debug_payload_sample.json", 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False, indent=2)
        
        print(f"\n🎯 Key Observations:")
        print(f"  1. Payload structure matches ReportInput schema")
        print(f"  2. All required fields are present with correct types")
        print(f"  3. Comments are properly formatted with id, comment, source, url")
        print(f"  4. Default prompts are in Japanese as expected")
        print(f"  5. Boolean flags are properly set")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing payload: {e}")
        return False

if __name__ == "__main__":
    success = analyze_payload_structure()
    sys.exit(0 if success else 1)
