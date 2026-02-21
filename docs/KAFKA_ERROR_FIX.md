# Kafkaエラー修正ガイド

**作成日**: 2026年1月29日

---

## 🔧 問題

バックエンド起動時に以下のエラーが発生：

```
ModuleNotFoundError: No module named 'kafka.vendor.six.moves'
```

---

## ✅ 修正内容

### 1. sixパッケージの追加

`requirements.txt`に`six==1.16.0`を追加しました。

### 2. Kafkaインポートのオプショナル化

`backend/event_streaming/kafka_client.py`を修正：

- Kafkaが利用できない場合でもエラーで停止しない
- 警告を出して続行
- 実際にKafkaを使用する際にエラーを発生

### 3. main.pyの修正

`main.py`でのイベントストリーミングモジュールのインポートをオプショナル化：

- Kafkaが利用できない場合でもアプリケーションは起動
- イベントストリーミング機能のみが無効化

---

## 🚀 解決方法

### 方法1: sixパッケージをインストール（推奨）

```cmd
cd backend
venv\Scripts\activate
pip install six==1.16.0
```

### 方法2: 依存パッケージを再インストール

```cmd
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

### 方法3: 仮想環境を再作成（最も確実）

```cmd
cd backend
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📝 確認

修正後、バックエンドを起動：

```cmd
cd backend
python main.py
```

以下のURLにアクセスして動作確認：

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ヘルスチェック**: http://localhost:8000/health

---

## ⚠️ 注意事項

- Kafkaが利用できない場合、イベントストリーミング機能は無効化されます
- 他の機能（MLOps、生成AI、セキュリティ等）は正常に動作します
- Kafkaが必要な場合は、`six`パッケージをインストールしてください

---

以上
