# 統合データレイク

**作成日**: 2026年1月29日  
**Phase**: 1.3

---

## 📋 概要

UEP v5.0の統合データレイクは、MinIOを使用して以下の機能を提供します：

- **オブジェクトストレージ**: S3互換のオブジェクトストレージ
- **データカタログ**: データのメタデータ管理
- **データガバナンス**: データのライフサイクル管理、アクセス制御

---

## 🏗️ アーキテクチャ

```
infrastructure/data-lake/
├── README.md            # このファイル
└── minio-config/       # MinIO設定（将来）

backend/data_lake/
├── __init__.py          # モジュール初期化
├── minio_client.py      # MinIOクライアント
├── catalog.py           # データカタログ
├── governance.py        # データガバナンス
├── models.py            # データモデル
└── routes.py            # APIエンドポイント
```

---

## 🔧 MinIO設定

### 接続情報

- **エンドポイント**: `http://minio:9000`
- **コンソール**: `http://localhost:9001`
- **ユーザー名**: `minioadmin`
- **パスワード**: `minioadmin`

### バケット構成

- `raw-data`: 生データ
- `processed-data`: 処理済みデータ
- `ml-models`: MLモデル
- `datasets`: データセット
- `backups`: バックアップ

---

## 📝 APIエンドポイント

### データレイク管理

- `GET /api/v1/data-lake/buckets` - バケット一覧
- `POST /api/v1/data-lake/buckets` - バケット作成
- `DELETE /api/v1/data-lake/buckets/{bucket_name}` - バケット削除
- `GET /api/v1/data-lake/buckets/{bucket_name}/objects` - オブジェクト一覧
- `POST /api/v1/data-lake/buckets/{bucket_name}/upload` - ファイルアップロード
- `GET /api/v1/data-lake/buckets/{bucket_name}/objects/{object_name}` - ファイルダウンロード

### データカタログ

- `GET /api/v1/data-lake/catalog` - カタログ一覧
- `POST /api/v1/data-lake/catalog` - カタログ登録
- `GET /api/v1/data-lake/catalog/{catalog_id}` - カタログ詳細
- `PUT /api/v1/data-lake/catalog/{catalog_id}` - カタログ更新

### データガバナンス

- `GET /api/v1/data-lake/governance/policies` - ポリシー一覧
- `POST /api/v1/data-lake/governance/policies` - ポリシー作成
- `GET /api/v1/data-lake/governance/lifecycle` - ライフサイクル管理

---

## 🚀 使用方法

### MinIOコンソールへのアクセス

1. ブラウザで `http://localhost:9001` にアクセス
2. ユーザー名: `minioadmin`、パスワード: `minioadmin` でログイン

### API経由での操作

```bash
# バケット一覧取得
curl -X GET "http://localhost:8000/api/v1/data-lake/buckets" \
  -H "Authorization: Bearer <access_token>"

# バケット作成
curl -X POST "http://localhost:8000/api/v1/data-lake/buckets" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"name": "my-bucket"}'
```

---

## 📚 参考資料

- [MinIO Documentation](https://min.io/docs/)
- [AWS S3 API Compatibility](https://min.io/docs/minio/linux/reference/minio-mc/mc.html)

---

以上
