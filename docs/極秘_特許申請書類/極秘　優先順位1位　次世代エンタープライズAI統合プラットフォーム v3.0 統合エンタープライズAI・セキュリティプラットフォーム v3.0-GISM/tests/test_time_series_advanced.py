"""
時系列分析サービスのテスト（高度な手法）
フェーズ2: 専門領域統合
"""
import pytest
import numpy as np
from app.services.time_series_advanced import TimeSeriesAdvancedService


@pytest.fixture
def time_series_service():
    """TimeSeriesAdvancedServiceのインスタンス"""
    return TimeSeriesAdvancedService()


@pytest.fixture
def sample_time_series():
    """サンプル時系列データ"""
    # トレンド付き時系列データを生成
    t = np.arange(0, 50)
    trend = 0.1 * t
    noise = np.random.normal(0, 0.5, 50)
    return (trend + noise).tolist()


@pytest.fixture
def sample_multivariate_data():
    """サンプル多変量時系列データ"""
    return [
        {"temperature": 20.0 + i * 0.1, "humidity": 50.0 + i * 0.2, "pressure": 1013.0 + i * 0.05}
        for i in range(30)
    ]


@pytest.fixture
def sample_time_series_list():
    """サンプル時系列データのリスト"""
    return [
        [1.0, 2.0, 3.0, 4.0, 5.0],
        [10.0, 11.0, 12.0, 13.0, 14.0],
        [20.0, 21.0, 22.0, 23.0, 24.0],
        [5.0, 6.0, 7.0, 8.0, 9.0]
    ]


def test_time_series_service_initialization(time_series_service):
    """サービス初期化テスト"""
    assert time_series_service is not None
    assert hasattr(time_series_service, 'is_available')


def test_is_available(time_series_service):
    """利用可能性チェックテスト"""
    result = time_series_service.is_available()
    assert isinstance(result, bool)


def test_predict_time_series(time_series_service, sample_time_series):
    """時系列予測テスト"""
    result = time_series_service.predict_time_series(sample_time_series, horizon=5)
    
    assert "status" in result
    if result["status"] == "success":
        assert "forecast" in result
        assert "horizon" in result
    elif result["status"] == "error":
        assert "message" in result


def test_predict_time_series_simple_method(time_series_service, sample_time_series):
    """時系列予測テスト（簡易手法）"""
    result = time_series_service.predict_time_series(sample_time_series, horizon=5, method="simple")
    
    assert "status" in result
    if result["status"] == "success":
        assert "forecast" in result
        assert len(result["forecast"]) == 5


def test_detect_anomalies(time_series_service, sample_time_series):
    """異常検知テスト"""
    result = time_series_service.detect_anomalies(sample_time_series)
    
    assert "status" in result
    if result["status"] == "success":
        assert "anomalies" in result
        assert "anomaly_count" in result
    elif result["status"] == "error":
        assert "message" in result


def test_detect_anomalies_statistical(time_series_service, sample_time_series):
    """異常検知テスト（統計的手法）"""
    result = time_series_service.detect_anomalies(sample_time_series, method="statistical")
    
    assert "status" in result
    if result["status"] == "success":
        assert "anomalies" in result
        assert "anomaly_count" in result


def test_predict_multivariate(time_series_service, sample_multivariate_data):
    """多変量時系列予測テスト"""
    result = time_series_service.predict_multivariate(
        sample_multivariate_data,
        "temperature",
        horizon=5
    )
    
    assert "status" in result
    if result["status"] == "success":
        assert "forecast" in result
        assert "target_variable" in result
    elif result["status"] == "error":
        assert "message" in result


def test_cluster_time_series(time_series_service, sample_time_series_list):
    """時系列クラスタリングテスト"""
    result = time_series_service.cluster_time_series(sample_time_series_list, n_clusters=2)
    
    assert "status" in result
    if result["status"] == "success":
        assert "clusters" in result
        assert "n_clusters" in result
    elif result["status"] == "error":
        assert "message" in result


def test_predict_time_series_insufficient_data(time_series_service):
    """データ不足のテスト"""
    short_data = [1.0, 2.0, 3.0]  # 10未満
    result = time_series_service.predict_time_series(short_data, horizon=5)
    
    assert "status" in result
    assert result["status"] == "error"
    assert "message" in result
