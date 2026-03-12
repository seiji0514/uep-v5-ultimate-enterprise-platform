"""
設定ファイル（統合版）
"""
import os
from dotenv import load_dotenv

load_dotenv()

# サーバー設定
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
# ポートが使用中の場合は自動で別のポートを検出
DEFAULT_PORT = int(os.getenv("SERVER_PORT", "8001"))

def get_available_port(start_port: int = DEFAULT_PORT) -> int:
    """使用可能なポートを取得"""
    import socket
    port = start_port
    max_attempts = 10
    for _ in range(max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            port += 1
    return start_port  # フォールバック

SERVER_PORT = get_available_port(DEFAULT_PORT)
if SERVER_PORT != DEFAULT_PORT:
    import logging
    logging.warning(f"ポート{DEFAULT_PORT}が使用中のため、ポート{SERVER_PORT}を使用します。")

# OpenAI設定
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# 音声認識設定
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base")

# 音声合成設定
TTS_ENGINE = os.getenv("TTS_ENGINE", "pyttsx3")  # pyttsx3 or transformers

# ログ設定
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
