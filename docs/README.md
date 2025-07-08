# kouchou-ai ドキュメント

このディレクトリには、kouchou-aiサービスの使用方法とAPI仕様に関するドキュメントが含まれています。

## ドキュメント一覧

### [API レポート自動化ガイド](./api-report-automation.md)
- API経由でのレポート生成自動化の完全ガイド
- 自動化スクリプトの使用方法
- 設定ファイルの作成方法
- トラブルシューティング

## クイックスタート

### 1. 環境設定
```bash
export ADMIN_API_KEY="your-admin-api-key"
```

### 2. CSVファイル準備
```csv
text,url
"プルリクエストの内容","https://github.com/..."
```

### 3. レポート作成

#### 単一レポート作成
```bash
cd scripts
python create_second_report.py
```

#### インテリジェント自動化（推奨）
```bash
cd scripts
python intelligent_report_automation.py
```

### 4. 進捗確認
管理画面: https://client-admin.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io/

## サポート

- GitHub Issues: [kouchou-ai Issues](https://github.com/team-mirai/kouchou-ai/issues)
- 実装例: [scripts/](../scripts/) ディレクトリ
