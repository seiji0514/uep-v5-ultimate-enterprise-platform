# CI/CDエラー修正ガイド

**作成日**: 2026年1月29日

---

## 🔧 問題

バックエンド起動時に以下のエラーが発生：

```
NameError: name 'CICDPipeline' is not defined
```

---

## ✅ 修正内容

### 1. クラス名の競合を解決

`backend/idop/cicd.py`を修正：

- `CICDPipelineModel`（Pydanticモデル）と`CICDPipeline`（管理クラス）を明確に分離
- 型注釈を`CICDPipelineModel`に統一

### 2. routes.pyの修正

`backend/idop/routes.py`を修正：

- `List[CICDPipeline]`を`List[CICDPipelineModel]`に変更

### 3. __init__.pyの修正

`backend/idop/__init__.py`を修正：

- `CICDPipelineModel`もエクスポート

---

## 🚀 再起動

修正後、バックエンドを再起動：

```cmd
cd backend
python main.py
```

または：

```cmd
start-backend.bat
```

---

## 📝 確認

以下のURLにアクセスして動作確認：

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ヘルスチェック**: http://localhost:8000/health

---

以上
