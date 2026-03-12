"""
音声応答サービス（統合版）
既存の音声応答サービスを統合
"""
import sys
from pathlib import Path

# 既存の音声応答サービスをインポート
# unified-platform/backend/services/voice_response_service.py から
# ワークスペースルートまで: ../../../
_current_file = Path(__file__).resolve()
PROJECT_ROOT = _current_file.parent.parent.parent.parent
voice_service_path = PROJECT_ROOT / "ai-voice-response-system" / "backend" / "services"

# デバッグ用
import logging
_logger = logging.getLogger(__name__)
_logger.debug(f"PROJECT_ROOT: {PROJECT_ROOT}")
_logger.debug(f"音声サービスパス: {voice_service_path} (存在: {voice_service_path.exists()})")

if voice_service_path.exists():
    sys.path.insert(0, str(voice_service_path))

try:
    from voice_response_service import VoiceResponseService as BaseVoiceResponseService
except ImportError:
    # フォールバック: 簡易実装
    import logging
    logger = logging.getLogger(__name__)
    logger.warning("既存の音声応答サービスが見つかりません。簡易実装を使用します。")
    
    class BaseVoiceResponseService:
        async def transcribe_audio_chunk(self, audio_chunk, connection_id):
            return {"status": "success", "text": ""}
        
        async def generate_response(self, text, connection_id):
            return f"応答: {text}"
        
        async def text_to_speech(self, text):
            return {"status": "success", "audio_data": None}


class VoiceResponseService(BaseVoiceResponseService):
    """
    統合版音声応答サービス
    既存のサービスを継承・拡張
    """
    pass
