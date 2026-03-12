# プロジェクト構造

```
ai-voice-response-system/
├── backend/                    # バックエンドサーバー
│   ├── main.py                # FastAPIサーバー（メイン）
│   └── services/              # サービス層
│       ├── __init__.py
│       └── voice_response_service.py  # 音声応答サービス
│
├── static/                     # 静的ファイル（フロントエンド）
│   └── index.html            # メインUI
│
├── config.py                  # 設定ファイル
├── requirements.txt          # Python依存関係
├── .env.example             # 環境変数テンプレート（.gitignore対象）
├── .gitignore               # Git除外設定
│
├── README.md                # プロジェクト概要
├── INSTALL.md               # インストールガイド
├── 実装ガイド.md            # 実装詳細ガイド
├── PROJECT_STRUCTURE.md     # このファイル
│
├── start.bat                # Windows起動スクリプト
└── start.sh                 # Linux/Mac起動スクリプト
```

## 主要ファイルの説明

### バックエンド

- **backend/main.py**: FastAPIサーバーのメインファイル
  - WebSocketエンドポイント
  - 静的ファイル配信
  - ルーティング設定

- **backend/services/voice_response_service.py**: 音声応答サービスのコア
  - 音声認識（Whisper）
  - AI応答生成（GPT）
  - 音声合成（TTS）
  - 会話履歴管理

### フロントエンド

- **static/index.html**: シングルページアプリケーション
  - Web Audio APIでマイク入力
  - WebSocketでリアルタイム通信
  - 会話UI表示

### 設定

- **config.py**: アプリケーション設定
  - 環境変数の読み込み
  - デフォルト値の設定

- **requirements.txt**: Pythonパッケージ依存関係

## データフロー

```
ユーザー音声入力
    ↓
[ブラウザ] Web Audio API
    ↓ WebSocket (音声データ)
[バックエンド] voice_response_service
    ├→ transcribe_audio_chunk() → テキスト
    ├→ generate_response() → 応答テキスト
    └→ text_to_speech() → 音声データ
    ↓ WebSocket (音声データ)
[ブラウザ] AudioContext
    ↓
ユーザー音声出力
```

## 拡張ポイント

1. **新しいTTSエンジンの追加**: `voice_response_service.py`の`text_to_speech()`メソッド
2. **新しいAIモデルの追加**: `generate_response()`メソッド
3. **UIのカスタマイズ**: `static/index.html`
4. **新しいエンドポイントの追加**: `backend/main.py`
