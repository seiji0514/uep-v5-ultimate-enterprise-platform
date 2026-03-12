# 統合セキュリティ・防衛プラットフォーム

UEP v5.0・統合基盤に属さない**個別システム**。UEP 起動時には含まれない。

**詳細**: [docs/起動方法と使用方法.md](../docs/起動方法と使用方法.md)

## 起動方法（個別）

### 1. バックエンド（API）

```cmd
cd security_defense_platform
start-backend.bat
```

- **ポート**: 9001
- **API**: http://localhost:9001/api/v1/security-defense-platform
- **Docs**: http://localhost:9001/docs

※ UEP の backend/venv を利用するため、初回は UEP の `start-backend.bat` で venv を作成してください。

### 2. フロントエンド

```cmd
cd security_defense_platform
start-frontend.bat
```

または PowerShell の場合:

```powershell
cd security_defense_platform
.\start-frontend.ps1
```

- **ポート**: 3001
- **URL**: http://localhost:3001

※ バックエンド（ポート9001）を先に起動してください。

## 構成

```
security_defense_platform/
├── README.md
├── main.py              ← 個別起動用（API）
├── start-backend.bat    ← バックエンド起動
├── start-frontend.bat   ← フロントエンド起動
├── start-frontend.ps1   ← フロントエンド起動（PowerShell）
├── backend/
│   ├── __init__.py
│   └── routes.py
└── frontend/
    ├── package.json
    ├── src/
    │   ├── App.tsx
    │   ├── api/
    │   └── components/
    └── public/
```

## 内部実装（参照）

- `backend/security_center/` - イベント・インシデント・リスク・Falco
- `backend/cyber_defense/` - IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス
