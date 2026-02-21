# 422エラー修正ガイド（デコレータ問題）

**作成日**: 2026年1月30日

---

## 問題の症状

APIリクエストが422エラー（Unprocessable Entity）で失敗する

エラーメッセージ: 「バリデーションエラー: query.args: 必須フィールド、query.kwargs: 必須フィールド」

---

## 原因

`require_permission`デコレータが`*args`と`**kwargs`を使用していたため、FastAPIが関数のシグネチャを正しく認識できず、`args`と`kwargs`をクエリパラメータとして解釈していました。

---

## 修正内容

### 1. `require_permission`デコレータの修正

`backend/auth/rbac.py`の`require_permission`デコレータを修正：

- `inspect.signature`を使用して元の関数のシグネチャを保持
- `functools.wraps`を使用して関数のメタデータを保持
- `wrapper.__signature__`を設定してFastAPIが正しく認識できるように

### 2. `require_role`デコレータの修正

同様に`require_role`デコレータも修正：

- FastAPI互換の実装に変更
- 関数のシグネチャを正しく保持

---

## 修正手順

### ステップ1: バックエンドを再起動

```cmd
# 現在のバックエンドを停止（Ctrl+C）
# その後、再起動
start-backend.bat
```

### ステップ2: フロントエンドを再読み込み

1. ブラウザでフロントエンドを再読み込み（F5）
2. MLOpsページにアクセス
3. エラーが解消されているか確認

---

## 確認方法

### Swagger UIで確認

1. `http://localhost:8000/docs` にアクセス
2. `/api/v1/mlops/pipelines` エンドポイントを開く
3. "Try it out"をクリック
4. "Execute"をクリック
5. 422エラーが発生しないことを確認

### フロントエンドで確認

1. `http://localhost:3000/mlops` にアクセス
2. パイプラインタブが正常に表示されることを確認
3. エラーメッセージが表示されないことを確認

---

## 技術的な詳細

### FastAPIのデコレータの要件

FastAPIでデコレータを使用する際は、以下の要件を満たす必要があります：

1. **関数のシグネチャを保持**: `inspect.signature`を使用
2. **メタデータを保持**: `functools.wraps`を使用
3. **`__signature__`属性を設定**: FastAPIが認識できるように

### 修正前の問題

```python
async def wrapper(*args, current_user: dict = Depends(get_current_user), **kwargs):
```

この実装では、FastAPIが`args`と`kwargs`をクエリパラメータとして解釈してしまいます。

### 修正後の実装

```python
@wraps(func)
async def wrapper(*args, **kwargs):
    sig = inspect.signature(func)
    bound = sig.bind(*args, **kwargs)
    # ... パーミッションチェック ...
    return await func(*bound.args, **bound.kwargs)

wrapper.__signature__ = sig
```

これにより、FastAPIが元の関数のシグネチャを正しく認識できます。

---

## トラブルシューティング

### 問題1: まだ422エラーが発生する

**解決方法:**
1. バックエンドを完全に再起動
2. ブラウザのキャッシュをクリア
3. フロントエンドを再読み込み

### 問題2: 他のエラーが発生する

**解決方法:**
1. ブラウザのコンソールでエラーの詳細を確認
2. バックエンドのログを確認
3. Swagger UIでAPIエンドポイントを直接テスト

---

## 確認事項

修正後、以下を確認してください：

- ✅ 422エラーが発生しない
- ✅ MLOpsページが正常に表示される
- ✅ パイプライン一覧が取得できる
- ✅ 他のページも正常に動作する

---

以上
