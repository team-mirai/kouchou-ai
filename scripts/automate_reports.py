#!/usr/bin/env python3
"""
Report Automation Script for kouchou-ai

This script automates the creation of multiple reports using the kouchou-ai API.
It processes reports sequentially to avoid memory issues and provides progress tracking.
"""

import os
import json
import requests
import csv
import time
import sys
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ReportConfig:
    """Configuration for a single report"""
    input: str  # Report ID
    question: str  # Report title
    intro: str  # Report description
    csv_file_path: str  # Path to CSV data file
    cluster: List[int]  # [level1, level2] cluster numbers
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    workers: int = 1
    is_pubcom: bool = False
    is_embedded_at_local: bool = False
    enable_source_link: bool = True
    local_llm_address: Optional[str] = None


class KouchouAIClient:
    """Client for interacting with the kouchou-ai API"""
    
    def __init__(self, api_base_url: str, admin_api_key: str):
        self.api_base_url = api_base_url.rstrip('/')
        self.admin_api_key = admin_api_key
        self.session = requests.Session()
        self.session.headers.update({
            "x-api-key": self.admin_api_key,
            "Content-Type": "application/json"
        })
    
    def create_report(self, config: ReportConfig) -> bool:
        """Create a report using the API"""
        try:
            comments = self._load_csv_data(config.csv_file_path)
            if not comments:
                print(f"  ✗ No comments found in {config.csv_file_path}")
                return False
            
            print(f"  → Loaded {len(comments)} comments from CSV")
            
            payload = {
                "input": config.input,
                "question": config.question,
                "intro": config.intro,
                "comments": comments,
                "cluster": config.cluster,
                "provider": config.provider,
                "model": config.model,
                "workers": config.workers,
                "prompt": self._get_default_prompts(),
                "is_pubcom": config.is_pubcom,
                "inputType": "file",
                "is_embedded_at_local": config.is_embedded_at_local,
                "enable_source_link": config.enable_source_link
            }
            
            if config.local_llm_address:
                payload["local_llm_address"] = config.local_llm_address
            
            response = self.session.post(
                f"{self.api_base_url}/admin/reports",
                json=payload,
                timeout=30
            )
            
            if response.status_code in [200, 202]:
                print(f"  ✓ Report creation started successfully (HTTP {response.status_code})")
                return True
            else:
                print(f"  ✗ API request failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"  ✗ Error creating report: {e}")
            return False
    
    def _load_csv_data(self, csv_file_path: str) -> List[Dict[str, Any]]:
        """Load and parse CSV data into the required comment format"""
        comments = []
        
        if not os.path.exists(csv_file_path):
            raise FileNotFoundError(f"CSV file not found: {csv_file_path}")
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for index, row in enumerate(reader):
                if "text" in row and "url" in row:
                    comment = {
                        "id": f"pr-{index + 1}",
                        "comment": row.get("text", ""),
                        "source": "GitHub PR",
                        "url": row.get("url", "")
                    }
                else:
                    comment = {
                        "id": row.get("id", f"csv-{index + 1}"),
                        "comment": row.get("comment", ""),
                        "source": row.get("source"),
                        "url": row.get("url")
                    }
                
                for key, value in row.items():
                    if key not in ["id", "comment", "source", "url", "text"] and value:
                        comment[f"attribute_{key}"] = value
                
                comments.append(comment)
        
        return comments
    
    def _get_default_prompts(self) -> Dict[str, str]:
        """Return default prompt settings"""
        return {
            "extraction": "以下のコメントから、主要な意見や提案を抽出してください。",
            "initial_labelling": "抽出された意見をグループ化してください。",
            "merge_labelling": "類似する意見グループを統合してください。",
            "overview": "全体的な分析結果をまとめてください。"
        }
    
    def get_report_status(self, report_id: str) -> Dict[str, Any]:
        """Get the status of a report"""
        try:
            response = self.session.get(
                f"{self.api_base_url}/admin/reports/{report_id}/status/step-json",
                timeout=10
            )
            if response.status_code == 200:
                return response.json()
            else:
                return {"current_step": "unknown", "error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"current_step": "unknown", "error": str(e)}


def load_report_configs(config_file: str) -> List[ReportConfig]:
    """Load report configurations from JSON file"""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"Configuration file not found: {config_file}")
    
    with open(config_file, 'r', encoding='utf-8') as f:
        config_data = json.load(f)
    
    configs = []
    for report_data in config_data.get("reports", []):
        config = ReportConfig(**report_data)
        configs.append(config)
    
    return configs


def validate_environment() -> tuple[str, str]:
    """Validate required environment variables"""
    api_base_url = os.getenv("KOUCHOU_AI_API_URL", "https://api.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io")
    admin_api_key = os.getenv("ADMIN_API_KEY")
    
    if not api_base_url:
        raise ValueError("KOUCHOU_AI_API_URL environment variable is required")
    
    if not admin_api_key:
        raise ValueError("ADMIN_API_KEY environment variable is required")
    
    return api_base_url, admin_api_key


def main():
    """Main function to process all reports"""
    print("🚀 Starting kouchou-ai Report Automation")
    print("=" * 50)
    
    try:
        api_base_url, admin_api_key = validate_environment()
        print(f"API URL: {api_base_url}")
        
        client = KouchouAIClient(api_base_url, admin_api_key)
        
        config_file = os.path.join(os.path.dirname(__file__), "report_configs.json")
        configs = load_report_configs(config_file)
        
        print(f"Loaded {len(configs)} report configurations")
        print()
        
        successful_reports = 0
        failed_reports = 0
        
        for i, config in enumerate(configs):
            print(f"📊 Creating report {i+1}/{len(configs)}: {config.input}")
            print(f"  Question: {config.question}")
            print(f"  CSV: {config.csv_file_path}")
            
            try:
                success = client.create_report(config)
                if success:
                    successful_reports += 1
                    print(f"  ✅ Report {config.input} creation started")
                else:
                    failed_reports += 1
                    print(f"  ❌ Failed to create report {config.input}")
            except Exception as e:
                failed_reports += 1
                print(f"  ❌ Error creating report {config.input}: {e}")
            
            if i < len(configs) - 1:
                print(f"  ⏳ Waiting 30 seconds before next report...")
                time.sleep(30)
            
            print()
        
        print("=" * 50)
        print("📈 Batch Report Creation Summary")
        print(f"✅ Successful: {successful_reports}")
        print(f"❌ Failed: {failed_reports}")
        print(f"📊 Total: {len(configs)}")
        
        if failed_reports > 0:
            print("\n⚠️  Some reports failed to create. Check the logs above for details.")
            sys.exit(1)
        else:
            print("\n🎉 All reports created successfully!")
            
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
