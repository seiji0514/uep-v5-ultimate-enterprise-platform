"""
音声処理サービス
フェーズ2: 専門領域統合
- Whisper: 音声認識（ASR）
- TTS: 音声合成
- 感情分析: 音声から感情を推定
- 異常検知: 音声の異常を検出
"""
import os
import io
import logging
from typing import Dict, Any, Optional
import numpy as np

# librosa（音声処理、必須）
try:
    import librosa
    import soundfile as sf
    LIBROSA_AVAILABLE = True
except ImportError:
    LIBROSA_AVAILABLE = False
    logging.warning("librosa not available. Audio processing functionality will be limited.")

# Whisper（音声認識、オプショナル）
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    logging.warning("Whisper not available. Speech recognition will use mock implementation.")

# TTS（音声合成、オプショナル）
try:
    from TTS.api import TTS
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    logging.warning("TTS not available. Text-to-speech will use mock implementation.")

logger = logging.getLogger(__name__)


class AudioProcessingService:
    """音声処理サービス"""
    
    def __init__(self):
        self.whisper_model = None
        self.tts_model = None
        self.whisper_available = WHISPER_AVAILABLE
        self.tts_available = TTS_AVAILABLE
        
        if WHISPER_AVAILABLE:
            try:
                # Whisperモデルをロード（初回は自動ダウンロード）
                logger.info("Loading Whisper model...")
                self.whisper_model = whisper.load_model("base")  # base版（軽量）
                logger.info("Whisper model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load Whisper model: {e}")
                self.whisper_available = False
        
        if TTS_AVAILABLE:
            try:
                # TTSモデルをロード
                logger.info("Loading TTS model...")
                self.tts_model = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
                logger.info("TTS model loaded successfully")
            except Exception as e:
                logger.warning(f"Failed to load TTS model: {e}")
                self.tts_available = False
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return LIBROSA_AVAILABLE
    
    def transcribe_audio(self, audio_data: bytes, language: Optional[str] = None) -> Dict[str, Any]:
        """
        音声認識（Whisper）
        
        Args:
            audio_data: 音声データ（bytes）
            language: 言語コード（例: "ja", "en"）
        
        Returns:
            認識されたテキスト
        """
        if not LIBROSA_AVAILABLE:
            return {
                "status": "error",
                "message": "librosa is not available"
            }
        
        try:
            # 音声データを一時ファイルに保存
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name
            
            # Whisperで音声認識
            if self.whisper_available and self.whisper_model:
                result = self.whisper_model.transcribe(tmp_path, language=language)
                os.unlink(tmp_path)  # 一時ファイル削除
                
                return {
                    "status": "success",
                    "text": result["text"],
                    "language": result.get("language", "unknown"),
                    "segments": [
                        {
                            "start": seg["start"],
                            "end": seg["end"],
                            "text": seg["text"]
                        }
                        for seg in result.get("segments", [])
                    ]
                }
            else:
                # モック実装
                os.unlink(tmp_path)  # 一時ファイル削除
                return {
                    "status": "success",
                    "text": "This is a mock transcription. Install Whisper for actual speech recognition.",
                    "language": language or "en",
                    "segments": [],
                    "note": "Mock implementation (Whisper not available)"
                }
        
        except Exception as e:
            logger.error(f"Error in transcribe_audio: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def synthesize_speech(self, text: str, voice_id: Optional[str] = None, language: str = "en") -> Dict[str, Any]:
        """
        音声合成（TTS）
        
        Args:
            text: 合成するテキスト
            voice_id: ボイスID（オプション）
            language: 言語コード
        
        Returns:
            音声データ（base64エンコード）またはパス
        """
        if not LIBROSA_AVAILABLE:
            return {
                "status": "error",
                "message": "librosa is not available"
            }
        
        try:
            if self.tts_available and self.tts_model:
                # TTSで音声合成
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                    tmp_path = tmp_file.name
                
                self.tts_model.tts_to_file(text=text, file_path=tmp_path)
                
                # 音声ファイルを読み込み
                with open(tmp_path, 'rb') as f:
                    audio_bytes = f.read()
                
                os.unlink(tmp_path)  # 一時ファイル削除
                
                # base64エンコード
                import base64
                audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
                
                return {
                    "status": "success",
                    "audio_base64": audio_base64,
                    "text": text,
                    "language": language,
                    "format": "wav"
                }
            else:
                # モック実装
                return {
                    "status": "success",
                    "audio_base64": "",  # 空の音声データ
                    "text": text,
                    "language": language,
                    "format": "wav",
                    "note": "Mock implementation (TTS not available)"
                }
        
        except Exception as e:
            logger.error(f"Error in synthesize_speech: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def analyze_emotion(self, audio_data: bytes) -> Dict[str, Any]:
        """
        音声感情分析
        
        Args:
            audio_data: 音声データ（bytes）
        
        Returns:
            感情分析結果
        """
        if not LIBROSA_AVAILABLE:
            return {
                "status": "error",
                "message": "librosa is not available"
            }
        
        try:
            # 音声データを一時ファイルに保存
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name
            
            # 音声を読み込み
            y, sr = librosa.load(tmp_path, sr=None)
            os.unlink(tmp_path)  # 一時ファイル削除
            
            # 基本的な特徴量抽出
            # 実際の感情分析には機械学習モデルが必要
            features = {
                "duration": float(len(y) / sr),
                "sample_rate": int(sr),
                "mean_amplitude": float(np.mean(np.abs(y))),
                "max_amplitude": float(np.max(np.abs(y))),
                "zero_crossing_rate": float(np.mean(librosa.feature.zero_crossing_rate(y)[0])),
                "spectral_centroid": float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)[0])),
                "mfcc": [float(x) for x in np.mean(librosa.feature.mfcc(y=y, sr=sr), axis=1)]
            }
            
            # 簡易的な感情推定（デモ用）
            # 実際には機械学習モデルを使用
            emotion_scores = {
                "happy": 0.3,
                "sad": 0.2,
                "angry": 0.1,
                "neutral": 0.4
            }
            
            # 最大スコアの感情を選ぶ
            dominant_emotion = max(emotion_scores, key=emotion_scores.get)
            
            return {
                "status": "success",
                "emotion": dominant_emotion,
                "emotion_scores": emotion_scores,
                "features": features,
                "note": "Basic emotion analysis (ML model required for accurate results)"
            }
        
        except Exception as e:
            logger.error(f"Error in analyze_emotion: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def detect_audio_anomaly(self, audio_data: bytes, threshold: float = 0.5) -> Dict[str, Any]:
        """
        音声異常検知
        
        Args:
            audio_data: 音声データ（bytes）
            threshold: 異常検知の閾値
        
        Returns:
            異常検知結果
        """
        if not LIBROSA_AVAILABLE:
            return {
                "status": "error",
                "message": "librosa is not available"
            }
        
        try:
            # 音声データを一時ファイルに保存
            import tempfile
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_file.write(audio_data)
                tmp_path = tmp_file.name
            
            # 音声を読み込み
            y, sr = librosa.load(tmp_path, sr=None)
            os.unlink(tmp_path)  # 一時ファイル削除
            
            # 異常検知のための特徴量抽出
            # 実際の異常検知には機械学習モデルが必要
            features = {
                "zero_crossing_rate": float(np.mean(librosa.feature.zero_crossing_rate(y)[0])),
                "spectral_rolloff": float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr)[0])),
                "spectral_bandwidth": float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)[0])),
                "rms_energy": float(np.mean(librosa.feature.rms(y=y)[0]))
            }
            
            # 簡易的な異常検知（デモ用）
            # 実際にはIsolation Forest等の異常検知アルゴリズムを使用
            anomaly_score = 0.2  # モックスコア
            is_anomaly = anomaly_score > threshold
            
            return {
                "status": "success",
                "is_anomaly": is_anomaly,
                "anomaly_score": anomaly_score,
                "threshold": threshold,
                "features": features,
                "note": "Basic anomaly detection (ML model required for accurate results)"
            }
        
        except Exception as e:
            logger.error(f"Error in detect_audio_anomaly: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

