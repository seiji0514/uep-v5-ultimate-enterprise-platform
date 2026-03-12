"""
統合APIゲートウェイ
すべての音声リクエストを統一的に処理
"""
import logging
from typing import Dict, Optional, Tuple

logger = logging.getLogger(__name__)


class UnifiedAPIGateway:
    """
    統合APIゲートウェイ
    
    機能:
    - 音声リクエストの統一処理
    - 分野別モジュールへのルーティング
    - 応答の統合
    """
    
    def __init__(self, voice_service, domain_manager):
        """
        初期化
        
        Args:
            voice_service: 音声応答サービス
            domain_manager: 分野管理サービス
        """
        self.voice_service = voice_service
        self.domain_manager = domain_manager
    
    async def process_voice_request(
        self,
        audio_chunk: bytes,
        domain: Optional[str],
        connection_id: int
    ) -> Tuple[Optional[bytes], str]:
        """
        音声リクエストを処理
        
        Args:
            audio_chunk: 音声データ
            domain: 分野（Noneの場合は汎用応答）
            connection_id: 接続ID
        
        Returns:
            (音声データ, 応答テキスト)
        """
        try:
            # 1. 音声認識
            transcription_result = await self.voice_service.transcribe_audio_chunk(
                audio_chunk, connection_id
            )
            
            if transcription_result.get("status") != "success":
                return None, "音声認識に失敗しました"
            
            text = transcription_result.get("text", "")
            if not text:
                return None, ""
            
            # 2. 分野別モジュールで処理
            if domain:
                response_text = await self.domain_manager.process_domain_query(
                    domain, text, connection_id
                )
            else:
                # 汎用応答生成
                response_text = await self.voice_service.generate_response(
                    text, connection_id
                )
            
            # 3. 音声合成
            audio_response = await self.voice_service.text_to_speech(response_text)
            
            if audio_response.get("status") == "success":
                audio_data = audio_response.get("audio_data")
                return audio_data, response_text
            else:
                return None, response_text
        
        except Exception as e:
            logger.error(f"統合音声処理エラー: {e}")
            return None, f"エラーが発生しました: {str(e)}"
