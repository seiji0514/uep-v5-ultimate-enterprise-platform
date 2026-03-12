# インストールガイド

## 必要な環境

- Python 3.8以上
- pip（Pythonパッケージマネージャー）
- マイク（音声入力用）
- スピーカーまたはヘッドフォン（音声出力用）

## セットアップ手順

### 1. プロジェクトのクローンまたはダウンロード

```bash
cd ai-voice-response-system
```

### 2. 仮想環境の作成（推奨）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

**注意**: 初回インストールには時間がかかります（特にtorchやtransformers）。

### 4. 環境変数の設定（オプション）

`.env`ファイルを作成：

```env
# OpenAI API Key（オプション）
# 設定すると、より高精度な音声認識と応答生成が可能です
OPENAI_API_KEY=your_api_key_here

# サーバー設定
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# Whisperモデル（tiny, base, small, medium, large）
WHISPER_MODEL=base

# AIモデル
AI_MODEL=gpt-3.5-turbo

# TTSエンジン（pyttsx3, transformers）
TTS_ENGINE=pyttsx3
```

**ローカルモデルのみ使用する場合**: `.env`ファイルは不要です。

### 5. サーバーの起動

```bash
# Windows
start.bat

# または手動で
cd backend
python main.py
```

### 6. ブラウザでアクセス

```
http://localhost:8000
```

## トラブルシューティング

### マイクが認識されない

1. ブラウザの設定でマイクの使用を許可してください
2. システムの音声設定を確認してください
3. 他のアプリケーションがマイクを使用していないか確認してください

### 音声認識が動作しない

1. Whisperが正しくインストールされているか確認：
   ```bash
   pip install openai-whisper
   ```

2. 初回起動時はモデルのダウンロードに時間がかかります

### 音声合成が動作しない

1. pyttsx3がインストールされているか確認：
   ```bash
   pip install pyttsx3
   ```

2. Windowsの場合、SAPI5が利用可能か確認してください
3. Linuxの場合、espeakまたはfestivalが必要です：
   ```bash
   # Ubuntu/Debian
   sudo apt-get install espeak
   ```

### ポートが既に使用されている

`.env`ファイルで別のポートを指定：
```env
SERVER_PORT=8001
```

## 動作確認

1. ブラウザで `http://localhost:8000` を開く
2. 「会話を開始」ボタンをクリック
3. マイクの使用を許可
4. マイクに向かって話す
5. AIが応答を返すことを確認

## 次のステップ

- [実装ガイド.md](実装ガイド.md) を読んで詳細を確認
- [README.md](README.md) で機能を確認
- カスタマイズや拡張を行う
