# スクリプト集

このディレクトリには、kouchou-aiプロジェクトの運用と管理に役立つスクリプトが含まれています。

## スクリプト一覧

### automate_reports.py
複数のレポートを順次作成するための自動化スクリプト。API経由でレポート作成を行います。

**特徴:**
- 順次処理によりメモリ問題を回避
- 進捗追跡とエラーハンドリング
- 管理者APIエンドポイントとの直接統合
- JSON設定ファイルによる設定可能なレポート設定

**使用方法:**
```bash
# 環境変数を設定
export ADMIN_API_KEY="your-admin-api-key"
export KOUCHOU_AI_API_URL="https://api.salmonpebble-febdd0ee.japaneast.azurecontainerapps.io"

# 自動化を実行
python automate_reports.py
```

### report_configs.json
作成するすべてのレポートを定義する設定ファイル。CSVデータパスと設定を含みます。

**重要:** メモリ問題を避けるため、レポートは30秒間隔で順次処理されます。並列処理は行わないでください。

### fetch_reports.py
既存のAPIサーバーからレポートデータを取得し、ローカル環境に保存するスクリプト。
新しい環境へのデータ移行に使用します。

### upload_reports_to_azure.py
ローカル環境のレポートデータをAzure Blob Storageにアップロードするスクリプト。
Azure環境への移行時に使用します。

### assign_storage_role.sh
Azure Blob Storageへのアクセス権限（Storage Blob Data Contributor）を
現在ログインしているユーザーに付与するスクリプト。

## 使用方法

各スクリプトの詳細な使用方法は、スクリプトファイル内のコメントを参照してください。
一般的な実行手順：

```bash
# レポートデータの取得
python scripts/fetch_reports.py --api-url https://your-api-url

# Azure Blob Storageへのアクセス権限付与
./scripts/assign_storage_role.sh

# レポートデータのAzure Blob Storageへのアップロード
python scripts/upload_reports_to_azure.py
```

## アップロード後のコンテナ再起動

レポートをアップロードした後、変更を反映させるにはAPIコンテナの再起動が必要です：

```bash
make azure-restart-api
```

再起動後、ブラウザをリロードすると、アップロードしたレポートが表示されます。
