# 完全統合AI音声応答プラットフォーム - インストールガイド

## 📋 前提条件

- Python 3.8以上
- pip
- マイク（音声入力用）

## 🚀 インストール手順

### 1. 依存パッケージのインストール

```bash
cd unified-platform
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env`ファイルを作成し、以下の設定を追加：

```env
# サーバー設定
SERVER_HOST=0.0.0.0
SERVER_PORT=8001

# OpenAI設定（オプション）
OPENAI_API_KEY=your_api_key_here

# 音声認識設定
WHISPER_MODEL=base

# 音声合成設定
TTS_ENGINE=pyttsx3
```

### 3. 既存システムとの統合（オプション）

既存の医療、法務、金融システムと統合する場合：

1. **医療システム**: `healthcare_ai.py`のパスを設定
2. **法務システム**: `contract-review-system`のパスを設定
3. **金融システム**: `fintech_ai.py`のパスを設定

各モジュールの`_initialize_*_service()`メソッドでパスを調整してください。

## 🎯 起動方法

### Windows

```bash
start.bat
```

### Linux/Mac

```bash
cd backend
python main.py
```

## 📖 使用方法

1. ブラウザで `http://localhost:8001` にアクセス
2. 分野を選択（医療、法務、金融など）
3. 「会話を開始」ボタンをクリック
4. マイクに向かって話す
5. AIが分野特化の応答を返します

## 🔧 トラブルシューティング

### マイクが認識されない

- ブラウザのマイク権限を確認
- HTTPS接続を使用（localhostは除く）

### 音声認識が動作しない

- Whisperモデルが正しくインストールされているか確認
- `WHISPER_MODEL`の設定を確認

### 音声合成が動作しない

- `pyttsx3`がインストールされているか確認
- `TTS_ENGINE`の設定を確認

## 📝 まとめ

完全統合AI音声応答プラットフォームのインストールが完了しました。
