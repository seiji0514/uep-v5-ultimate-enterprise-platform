# 統合セキュリティ基盤

**作成日**: 2026年1月29日  
**Phase**: 1.6

---

## 📋 概要

UEP v5.0の統合セキュリティ基盤は、以下の機能を提供します：

- **ゼロトラストアーキテクチャ**: すべての通信を検証・認証
- **mTLS**: 相互TLS認証によるサービス間通信のセキュア化
- **Vault**: シークレット管理と動的認証情報の管理

---

## 🏗️ アーキテクチャ

```
infrastructure/security/
├── README.md            # このファイル
├── vault-config/        # Vault設定（将来）
└── certificates/        # 証明書（将来）

backend/security/
├── __init__.py          # モジュール初期化
├── vault_client.py      # Vaultクライアント
├── zero_trust.py        # ゼロトラスト実装
├── mtls.py              # mTLS実装
├── policies.py          # セキュリティポリシー
└── routes.py            # セキュリティAPIエンドポイント
```

---

## 🔧 サービス設定

### HashiCorp Vault

- **URL**: http://localhost:8200
- **UI**: http://localhost:8200/ui
- **初期トークン**: `root` (開発環境のみ)
- **用途**: シークレット管理、動的認証情報

---

## 🔒 セキュリティ機能

### ゼロトラストアーキテクチャ

- すべてのリクエストの検証
- 最小権限の原則
- 継続的な検証

### mTLS (相互TLS認証)

- サービス間通信の暗号化
- クライアント証明書による認証
- 証明書の自動ローテーション

### Vault統合

- シークレットの安全な保存
- 動的認証情報の生成
- アクセストークンの管理

---

## 📝 APIエンドポイント

### セキュリティ管理

- `GET /api/v1/security/policies` - セキュリティポリシー一覧
- `POST /api/v1/security/policies` - セキュリティポリシー作成
- `GET /api/v1/security/secrets` - シークレット一覧（Vault経由）
- `POST /api/v1/security/secrets` - シークレット作成
- `GET /api/v1/security/certificates` - 証明書情報

---

## 🚀 使用方法

### Vault UIにアクセス

```bash
# Vault UIにアクセス
# http://localhost:8200/ui
# トークン: root (開発環境のみ)
```

### シークレットの取得

```bash
curl -X GET "http://localhost:8000/api/v1/security/secrets/database/password" \
  -H "Authorization: Bearer <access_token>" \
  -H "X-Vault-Token: <vault_token>"
```

---

## 📚 参考資料

- [HashiCorp Vault Documentation](https://www.vaultproject.io/docs)
- [Zero Trust Architecture](https://www.nist.gov/publications/zero-trust-architecture)
- [mTLS Guide](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/)

---

以上
