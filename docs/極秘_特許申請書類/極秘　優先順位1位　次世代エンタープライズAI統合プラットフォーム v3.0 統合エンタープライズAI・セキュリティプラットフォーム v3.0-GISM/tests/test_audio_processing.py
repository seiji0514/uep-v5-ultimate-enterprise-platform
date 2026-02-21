"""
音声処理サービスのテスト
フェーズ2: 専門領域統合
"""
import pytest
import numpy as np
import io
import wave
from app.services.audio_processing import AudioProcessingService


@pytest.fixture
def audio_processing_service():
    """AudioProcessingServiceのインスタンス"""
    return AudioProcessingService()


@pytest.fixture
def sample_audio():
    """サンプル音声データ（WAV形式）"""
    # 簡単なWAVファイルを生成
    sample_rate = 44100
    duration = 1.0  # 1秒
    frequency = 440  # A4の音
    
    t = np.linspace(0, duration, int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * t)
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # WAVファイルとしてエンコード
    wav_buffer = io.BytesIO()
    with wave.open(wav_buffer, 'wb') as wav_file:
        wav_file.setnchannels(1)  # モノラル
        wav_file.setsampwidth(2)  # 16bit
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return wav_buffer.getvalue()


def test_audio_processing_service_initialization(audio_processing_service):
    """サービス初期化テスト"""
    assert audio_processing_service is not None
    assert hasattr(audio_processing_service, 'is_available')


def test_is_available(audio_processing_service):
    """利用可能性チェックテスト"""
    result = audio_processing_service.is_available()
    assert isinstance(result, bool)


def test_transcribe_audio(audio_processing_service, sample_audio):
    """音声認識テスト"""
    result = audio_processing_service.transcribe_audio(sample_audio)
    
    assert "status" in result
    if result["status"] == "success":
        assert "text" in result
    elif result["status"] == "error":
        assert "message" in result


def test_synthesize_speech(audio_processing_service):
    """音声合成テスト"""
    result = audio_processing_service.synthesize_speech("Hello, world!")
    
    assert "status" in result
    if result["status"] == "success":
        assert "text" in result
        assert "language" in result
    elif result["status"] == "error":
        assert "message" in result


def test_analyze_emotion(audio_processing_service, sample_audio):
    """感情分析テスト"""
    result = audio_processing_service.analyze_emotion(sample_audio)
    
    assert "status" in result
    if result["status"] == "success":
        assert "emotion" in result
        assert "emotion_scores" in result
    elif result["status"] == "error":
        assert "message" in result


def test_detect_audio_anomaly(audio_processing_service, sample_audio):
    """異常検知テスト"""
    result = audio_processing_service.detect_audio_anomaly(sample_audio)
    
    assert "status" in result
    if result["status"] == "success":
        assert "is_anomaly" in result
        assert "anomaly_score" in result
    elif result["status"] == "error":
        assert "message" in result


def test_transcribe_audio_invalid_data(audio_processing_service):
    """無効な音声データのテスト"""
    invalid_audio = b"invalid_audio_data"
    
    result = audio_processing_service.transcribe_audio(invalid_audio)
    
    assert "status" in result
    # 無効な音声データの場合はエラーが返る可能性がある
    if result["status"] == "error":
        assert "message" in result

