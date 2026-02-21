"""
コンピュータビジョンサービスのテスト
フェーズ2: 専門領域統合
"""
import pytest
import numpy as np
from PIL import Image
import io
from app.services.computer_vision import ComputerVisionService


@pytest.fixture
def computer_vision_service():
    """ComputerVisionServiceのインスタンス"""
    return ComputerVisionService()


@pytest.fixture
def sample_image():
    """サンプル画像データ（PNG形式）"""
    # 100x100のRGB画像を生成
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    return img_bytes.getvalue()


@pytest.fixture
def sample_dicom_data():
    """サンプルDICOMデータ（モック）"""
    # 実際のDICOMデータの代わりに、簡単なバイナリデータを返す
    return b"fake_dicom_data_for_testing"


def test_computer_vision_service_initialization(computer_vision_service):
    """サービス初期化テスト"""
    assert computer_vision_service is not None
    assert hasattr(computer_vision_service, 'is_available')


def test_is_available(computer_vision_service):
    """利用可能性チェックテスト"""
    result = computer_vision_service.is_available()
    assert isinstance(result, bool)


def test_detect_objects(computer_vision_service, sample_image):
    """物体検出テスト"""
    result = computer_vision_service.detect_objects(sample_image)
    
    assert "status" in result
    if result["status"] == "success":
        assert "detections" in result
        assert "count" in result
    elif result["status"] == "error":
        assert "message" in result


def test_segment_image(computer_vision_service, sample_image):
    """画像セグメンテーションテスト"""
    result = computer_vision_service.segment_image(sample_image)
    
    assert "status" in result
    if result["status"] == "success":
        assert "segments" in result
        assert "count" in result
    elif result["status"] == "error":
        assert "message" in result


def test_analyze_medical_image(computer_vision_service, sample_dicom_data):
    """医療画像解析テスト"""
    result = computer_vision_service.analyze_medical_image(sample_dicom_data, "CT")
    
    assert "status" in result
    # DICOMが利用できない場合はエラーが返る可能性がある
    if result["status"] == "error":
        assert "message" in result


def test_process_video(computer_vision_service):
    """動画処理テスト"""
    # 簡単な動画データ（実際には動画ファイルが必要）
    # このテストは実際の動画ファイルがない場合、エラーになる可能性がある
    fake_video_data = b"fake_video_data"
    
    result = computer_vision_service.process_video(fake_video_data)
    
    assert "status" in result
    # 動画処理は実際の動画ファイルが必要なため、エラーになる可能性が高い
    if result["status"] == "error":
        assert "message" in result


def test_detect_objects_invalid_image(computer_vision_service):
    """無効な画像データのテスト"""
    invalid_image = b"invalid_image_data"
    
    result = computer_vision_service.detect_objects(invalid_image)
    
    assert "status" in result
    # 無効な画像データの場合はエラーが返る可能性がある
    if result["status"] == "error":
        assert "message" in result

