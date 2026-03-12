"""
設定ファイル
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# プロジェクトルート
BASE_DIR = Path(__file__).parent

# OpenAI API設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# サーバー設定
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8001"))  # デフォルトポート: 8001

# 音声認識設定
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")  # tiny, base, small, medium, large

# AI応答設定
AI_MODEL = os.getenv("AI_MODEL", "gpt-3.5-turbo")  # gpt-3.5-turbo, gpt-4
AI_MAX_TOKENS = int(os.getenv("AI_MAX_TOKENS", "200"))
AI_TEMPERATURE = float(os.getenv("AI_TEMPERATURE", "0.7"))

# TTS設定
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")  # pyttsx3, transformers, gtts

# 会話設定
MAX_CONVERSATION_HISTORY = int(os.getenv("MAX_CONVERSATION_HISTORY", "10"))
AUDIO_BUFFER_SIZE = int(os.getenv("AUDIO_BUFFER_SIZE", "5"))

# ログ設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
