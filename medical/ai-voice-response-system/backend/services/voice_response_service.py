"""
音声応答サービス
音声認識 → AI応答生成 → 音声合成の統合サービス
"""
import os
import logging
import asyncio
import base64
import tempfile
from typing import Dict, Optional, List
from collections import defaultdict
import io

logger = logging.getLogger(__name__)

# 音声認識（Whisper）
USE_OPENAI_API = False
try:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        USE_OPENAI_API = True
        openai_client = OpenAI(api_key=api_key)
except:
    pass

USE_LOCAL_WHISPER = False
try:
    import whisper
    USE_LOCAL_WHISPER = True
except ImportError:
    logger.warning("ローカルWhisperが利用できません")

# 音声合成（TTS）
# 優先順位: pyttsx3 > transformers
TTS_PYTTX3_AVAILABLE = False
TTS_TRANSFORMERS_AVAILABLE = False

try:
    import pyttsx3
    TTS_PYTTX3_AVAILABLE = True
    logger.info("pyttsx3が利用可能です")
except ImportError:
    logger.warning("pyttsx3が利用できません。インストールしてください: pip install pyttsx3")

try:
    import torch
    from transformers import pipeline
    import numpy as np
    TTS_TRANSFORMERS_AVAILABLE = True
    logger.info("transformers TTSが利用可能です")
except ImportError:
    logger.warning("transformers TTSが利用できません（オプション）")


class VoiceResponseService:
    """
    音声応答サービス
    
    機能:
    1. 音声認識（ASR）
    2. AI応答生成
    3. 音声合成（TTS）
    """
    
    def __init__(self):
        """サービス初期化"""
        self.whisper_model = None
        self.tts_engine = None  # pyttsx3エンジン
        self.tts_pipeline = None  # transformersパイプライン
        
        # 会話履歴管理（接続IDごと）
        self.conversation_history: Dict[int, List[Dict[str, str]]] = defaultdict(list)
        
        # 音声バッファ（接続IDごと）
        self.audio_buffers: Dict[int, List[bytes]] = defaultdict(list)
        
        # Whisperモデルの読み込み
        if USE_LOCAL_WHISPER:
            try:
                self.whisper_model = whisper.load_model("base")
                logger.info("ローカルWhisperモデルを読み込みました")
            except Exception as e:
                logger.error(f"Whisperモデルの読み込みに失敗: {e}")
        
        # TTSエンジンの初期化（優先順位: pyttsx3 > transformers）
        if TTS_PYTTX3_AVAILABLE:
            try:
                import pyttsx3
                self.tts_engine = pyttsx3.init()
                logger.info("pyttsx3エンジンを初期化しました")
            except Exception as e:
                logger.warning(f"pyttsx3の初期化に失敗: {e}")
                self.tts_engine = None
        
        # transformers TTSパイプラインの初期化（オプション）
        if TTS_TRANSFORMERS_AVAILABLE and self.tts_engine is None:
            try:
                self.tts_pipeline = pipeline(
                    "text-to-speech",
                    model="microsoft/speecht5_tts",
                    device=-1  # CPU使用
                )
                logger.info("transformers TTSパイプラインを初期化しました")
            except Exception as e:
                logger.warning(f"transformers TTSパイプラインの初期化に失敗: {e}")
                self.tts_pipeline = None
        
        # TTSが利用できない場合の警告
        if self.tts_engine is None and self.tts_pipeline is None:
            logger.warning("TTS機能が利用できません。音声合成は動作しません。")
            logger.info("インストール方法: pip install pyttsx3")
    
    async def transcribe_audio_chunk(
        self,
        audio_chunk: bytes,
        connection_id: int
    ) -> Dict:
        """
        音声チャンクを文字起こし
        
        Args:
            audio_chunk: 音声データ（バイナリ）
            connection_id: 接続ID
        
        Returns:
            文字起こし結果
        """
        try:
            # 音声チャンクをバッファに追加
            self.audio_buffers[connection_id].append(audio_chunk)
            
            # 一定量のデータが溜まったら処理
            # 簡易版: 毎回処理（実際は適切なバッファリングが必要）
            if len(self.audio_buffers[connection_id]) < 5:
                return {"status": "processing"}
            
            # バッファを結合
            audio_data = b''.join(self.audio_buffers[connection_id])
            self.audio_buffers[connection_id] = []
            
            # 一時ファイルに保存
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name
            
            try:
                # 音声認識
                if USE_OPENAI_API:
                    with open(tmp_path, "rb") as audio_file:
                        transcript = openai_client.audio.transcriptions.create(
                            model="whisper-1",
                            file=audio_file,
                            language="ja",
                            response_format="verbose_json"
                        )
                    text = transcript.text
                
                elif USE_LOCAL_WHISPER and self.whisper_model:
                    result = self.whisper_model.transcribe(tmp_path, language="ja")
                    text = result["text"]
                
                else:
                    return {
                        "status": "error",
                        "message": "音声認識機能が利用できません"
                    }
                
                # 空白や短すぎるテキストは無視
                text = text.strip()
                if len(text) < 2:
                    return {"status": "processing"}
                
                return {
                    "status": "success",
                    "text": text
                }
            
            finally:
                # 一時ファイルを削除
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        except Exception as e:
            logger.error(f"音声認識エラー: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def generate_response(
        self,
        user_text: str,
        connection_id: int
    ) -> Optional[str]:
        """
        AI応答を生成
        
        Args:
            user_text: ユーザーの発言
            connection_id: 接続ID
        
        Returns:
            AI応答テキスト
        """
        try:
            # 会話履歴に追加
            self.conversation_history[connection_id].append({
                "role": "user",
                "content": user_text
            })
            
            # 会話履歴を取得（最新10件）
            history = self.conversation_history[connection_id][-10:]
            
            # プロンプトを構築
            messages = [
                {"role": "system", "content": "あなたは親切で自然な会話ができるAIアシスタントです。簡潔で分かりやすい応答を心がけてください。"}
            ]
            
            for msg in history:
                if msg["role"] == "user":
                    messages.append({"role": "user", "content": msg["content"]})
                elif msg["role"] == "assistant":
                    messages.append({"role": "assistant", "content": msg["content"]})
            
            # OpenAI APIを使用
            if USE_OPENAI_API:
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    max_tokens=200,
                    temperature=0.7
                )
                ai_response = response.choices[0].message.content
            
            else:
                # フォールバック: 簡易応答
                ai_response = self._generate_simple_response(user_text)
            
            # 会話履歴に追加
            self.conversation_history[connection_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
        
        except Exception as e:
            logger.error(f"応答生成エラー: {e}")
            return "申し訳ございません。応答の生成に失敗しました。"
    
    def _generate_simple_response(self, user_text: str) -> str:
        """簡易応答生成（フォールバック）"""
        # キーワードベースの簡易応答
        user_text_lower = user_text.lower()
        
        if "こんにちは" in user_text or "こんばんは" in user_text:
            return "こんにちは！何かお手伝いできることはありますか？"
        elif "ありがとう" in user_text:
            return "どういたしまして！他にも何かありますか？"
        elif "さようなら" in user_text or "バイバイ" in user_text:
            return "さようなら！またお話しできるのを楽しみにしています。"
        elif "?" in user_text or "？" in user_text:
            return "その質問について、もう少し詳しく教えていただけますか？"
        else:
            return f"「{user_text}」についてですね。もう少し詳しく教えていただけますか？"
    
    async def text_to_speech(self, text: str) -> Dict:
        """
        テキストを音声に変換
        
        Args:
            text: テキスト
        
        Returns:
            音声データ（バイナリ）
        """
        try:
            # まず、初期化済みのpyttsx3エンジンを使用（優先）
            if self.tts_engine:
                try:
                    # 一時ファイルに保存
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_path = tmp_file.name
                    
                    self.tts_engine.save_to_file(text, tmp_path)
                    self.tts_engine.runAndWait()
                    
                    # ファイルを読み込む
                    with open(tmp_path, 'rb') as f:
                        audio_bytes = f.read()
                    
                    # 一時ファイルを削除
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    
                    return {
                        "status": "success",
                        "audio_data": audio_bytes,
                        "sample_rate": 22050  # pyttsx3のデフォルト
                    }
                except Exception as e:
                    logger.warning(f"pyttsx3での音声合成に失敗: {e}")
            
            # pyttsx3が利用できない場合、新規に初期化を試す
            elif TTS_PYTTX3_AVAILABLE:
                try:
                    import pyttsx3
                    engine = pyttsx3.init()
                    
                    # 一時ファイルに保存
                    import tempfile
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                        tmp_path = tmp_file.name
                    
                    engine.save_to_file(text, tmp_path)
                    engine.runAndWait()
                    
                    # ファイルを読み込む
                    with open(tmp_path, 'rb') as f:
                        audio_bytes = f.read()
                    
                    # 一時ファイルを削除
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                    
                    return {
                        "status": "success",
                        "audio_data": audio_bytes,
                        "sample_rate": 22050  # pyttsx3のデフォルト
                    }
                except Exception as e:
                    logger.warning(f"pyttsx3での音声合成に失敗: {e}")
            
            # 次に、transformersのTTSパイプラインを試す
            if self.tts_pipeline:
                try:
                    output = self.tts_pipeline(text)
                    
                    if isinstance(output, dict) and "audio" in output:
                        audio_array = output["audio"]
                        sample_rate = output.get("sampling_rate", 16000)
                        
                        # numpy配列をWAV形式のバイトに変換
                        import wave
                        
                        # 16bit PCMに変換
                        audio_int16 = (audio_array * 32767).astype(np.int16)
                        
                        # WAVファイル形式でバイト列を作成
                        wav_buffer = io.BytesIO()
                        with wave.open(wav_buffer, 'wb') as wav_file:
                            wav_file.setnchannels(1)  # モノラル
                            wav_file.setsampwidth(2)  # 16bit
                            wav_file.setframerate(sample_rate)
                            wav_file.writeframes(audio_int16.tobytes())
                        
                        audio_bytes = wav_buffer.getvalue()
                        
                        return {
                            "status": "success",
                            "audio_data": audio_bytes,
                            "sample_rate": sample_rate
                        }
                except Exception as e:
                    logger.warning(f"transformers TTSでの音声合成に失敗: {e}")
            
            # フォールバック: テキストのみ返す（音声なし）
            return {
                "status": "warning",
                "message": "TTS機能が利用できません。テキストのみ表示されます。",
                "text": text
            }
        
        except Exception as e:
            logger.error(f"音声合成エラー: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def start_conversation(self, connection_id: int):
        """会話を開始"""
        self.conversation_history[connection_id] = []
        self.audio_buffers[connection_id] = []
        logger.info(f"会話を開始しました: {connection_id}")
    
    async def end_conversation(self, connection_id: int):
        """会話を終了"""
        if connection_id in self.conversation_history:
            del self.conversation_history[connection_id]
        if connection_id in self.audio_buffers:
            del self.audio_buffers[connection_id]
        logger.info(f"会話を終了しました: {connection_id}")
    
    async def reset_conversation(self, connection_id: int):
        """会話履歴をリセット"""
        self.conversation_history[connection_id] = []
        logger.info(f"会話履歴をリセットしました: {connection_id}")
