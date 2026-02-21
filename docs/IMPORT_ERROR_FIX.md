# インポートエラー修正ガイド

**作成日**: 2026年1月29日

---

## 🔧 問題

バックエンド起動時に以下のエラーが発生：

```
NameError: name 'llm_client' is not defined
```

---

## ✅ 修正内容

### 1. 循環インポートの解決

`backend/generative_ai/rag.py`と`reasoning.py`を修正：

- `llm_client`のインポートを遅延評価に変更
- グローバルインスタンスの作成を遅延初期化に変更
- プロキシクラスを使用して後方互換性を維持

### 2. routes.pyの修正

`backend/generative_ai/routes.py`を修正：

- `get_rag_system()`と`get_reasoning_engine()`を使用
- 各エンドポイントで必要な時にインスタンスを取得

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

## ⚠️ 注意事項

- 循環インポートを防ぐため、グローバルインスタンスは遅延初期化されています
- 初回アクセス時に自動的に初期化されます
- エラーが発生した場合は、仮想環境を再作成してください

---

以上
