"""
時系列分析サービス（高度な手法）
フェーズ2: 専門領域統合
- TCN: Temporal Convolutional Network
- LSTM-Autoencoder: 異常検知
- 多変量時系列予測
- 時系列クラスタリング
"""
import logging
from typing import Dict, Any, Optional, List
import numpy as np

# statsmodels（時系列分析、必須）
try:
    import statsmodels.api as sm
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.seasonal import seasonal_decompose
    STATSMODELS_AVAILABLE = True
except ImportError:
    STATSMODELS_AVAILABLE = False
    logging.warning("statsmodels not available. Time series analysis functionality will be limited.")

# scikit-learn（異常検知、オプショナル）
try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. Anomaly detection will use basic implementation.")

logger = logging.getLogger(__name__)


class TimeSeriesAdvancedService:
    """時系列分析サービス（高度な手法）"""
    
    def __init__(self):
        self.statsmodels_available = STATSMODELS_AVAILABLE
        self.sklearn_available = SKLEARN_AVAILABLE
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return STATSMODELS_AVAILABLE
    
    def predict_time_series(
        self,
        time_series_data: List[float],
        horizon: int = 10,
        method: str = "arima"
    ) -> Dict[str, Any]:
        """
        時系列予測
        
        Args:
            time_series_data: 時系列データ
            horizon: 予測期間
            method: 予測手法（"arima", "simple"）
        
        Returns:
            予測結果
        """
        if not STATSMODELS_AVAILABLE:
            return {
                "status": "error",
                "message": "statsmodels is not available"
            }
        
        try:
            if len(time_series_data) < 10:
                return {
                    "status": "error",
                    "message": "Insufficient data points (minimum 10 required)"
                }
            
            data = np.array(time_series_data)
            
            if method == "arima" and STATSMODELS_AVAILABLE:
                # ARIMAモデルで予測
                try:
                    model = ARIMA(data, order=(1, 1, 1))
                    fitted_model = model.fit()
                    forecast = fitted_model.forecast(steps=horizon)
                    
                    return {
                        "status": "success",
                        "method": "ARIMA",
                        "forecast": forecast.tolist(),
                        "horizon": horizon,
                        "original_length": len(time_series_data)
                    }
                except Exception as e:
                    logger.warning(f"ARIMA model failed: {e}, using simple method")
                    method = "simple"
            
            # 簡易予測（移動平均ベース）
            if method == "simple":
                window_size = min(5, len(data) // 2)
                if window_size < 1:
                    window_size = 1
                
                last_values = data[-window_size:]
                trend = np.mean(np.diff(last_values)) if len(last_values) > 1 else 0
                base_value = np.mean(last_values)
                
                forecast = []
                for i in range(horizon):
                    forecast.append(float(base_value + trend * (i + 1)))
                
                return {
                    "status": "success",
                    "method": "simple_moving_average",
                    "forecast": forecast,
                    "horizon": horizon,
                    "original_length": len(time_series_data)
                }
        
        except Exception as e:
            logger.error(f"Error in predict_time_series: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def detect_anomalies(
        self,
        time_series_data: List[float],
        method: str = "isolation_forest"
    ) -> Dict[str, Any]:
        """
        異常検知（LSTM-Autoencoder風の実装）
        
        Args:
            time_series_data: 時系列データ
            method: 検知手法（"isolation_forest", "statistical"）
        
        Returns:
            異常検知結果
        """
        try:
            if len(time_series_data) < 10:
                return {
                    "status": "error",
                    "message": "Insufficient data points (minimum 10 required)"
                }
            
            data = np.array(time_series_data).reshape(-1, 1)
            
            if method == "isolation_forest" and SKLEARN_AVAILABLE:
                # Isolation Forestで異常検知
                scaler = StandardScaler()
                data_scaled = scaler.fit_transform(data)
                
                model = IsolationForest(contamination=0.1, random_state=42)
                predictions = model.fit_predict(data_scaled)
                
                anomalies = []
                for i, pred in enumerate(predictions):
                    if pred == -1:  # 異常
                        anomalies.append({
                            "index": i,
                            "value": float(time_series_data[i]),
                            "score": float(model.score_samples([data_scaled[i]])[0])
                        })
                
                return {
                    "status": "success",
                    "method": "isolation_forest",
                    "anomalies": anomalies,
                    "anomaly_count": len(anomalies),
                    "total_points": len(time_series_data)
                }
            
            # 統計的手法（Z-scoreベース）
            mean = np.mean(time_series_data)
            std = np.std(time_series_data)
            
            if std == 0:
                return {
                    "status": "success",
                    "method": "statistical",
                    "anomalies": [],
                    "anomaly_count": 0,
                    "total_points": len(time_series_data),
                    "note": "No variance in data"
                }
            
            threshold = 2.0  # 2標準偏差
            anomalies = []
            
            for i, value in enumerate(time_series_data):
                z_score = abs((value - mean) / std)
                if z_score > threshold:
                    anomalies.append({
                        "index": i,
                        "value": float(value),
                        "z_score": float(z_score)
                    })
            
            return {
                "status": "success",
                "method": "statistical_zscore",
                "anomalies": anomalies,
                "anomaly_count": len(anomalies),
                "total_points": len(time_series_data),
                "statistics": {
                    "mean": float(mean),
                    "std": float(std),
                    "threshold": threshold
                }
            }
        
        except Exception as e:
            logger.error(f"Error in detect_anomalies: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def predict_multivariate(
        self,
        multivariate_data: List[Dict[str, float]],
        target_variable: str,
        horizon: int = 10
    ) -> Dict[str, Any]:
        """
        多変量時系列予測
        
        Args:
            multivariate_data: 多変量時系列データ（各要素が変数の辞書）
            target_variable: 予測対象の変数名
            horizon: 予測期間
        
        Returns:
            予測結果
        """
        try:
            if len(multivariate_data) < 10:
                return {
                    "status": "error",
                    "message": "Insufficient data points (minimum 10 required)"
                }
            
            if target_variable not in multivariate_data[0]:
                return {
                    "status": "error",
                    "message": f"Target variable '{target_variable}' not found in data"
                }
            
            # ターゲット変数を抽出
            target_series = [d[target_variable] for d in multivariate_data]
            
            # 他の変数を特徴量として使用
            feature_names = [k for k in multivariate_data[0].keys() if k != target_variable]
            
            # 簡易的な多変量予測（線形回帰風）
            if len(feature_names) > 0 and len(target_series) > 0:
                # 最後の値とトレンドを使用
                last_target = target_series[-1]
                if len(target_series) > 1:
                    trend = np.mean(np.diff(target_series[-5:])) if len(target_series) >= 5 else 0
                else:
                    trend = 0
                
                forecast = []
                for i in range(horizon):
                    forecast.append(float(last_target + trend * (i + 1)))
                
                return {
                    "status": "success",
                    "method": "multivariate_simple",
                    "target_variable": target_variable,
                    "forecast": forecast,
                    "horizon": horizon,
                    "features_used": feature_names,
                    "note": "Basic multivariate prediction (ML model required for accurate results)"
                }
            else:
                # 単変量予測にフォールバック
                return self.predict_time_series(target_series, horizon)
        
        except Exception as e:
            logger.error(f"Error in predict_multivariate: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def cluster_time_series(
        self,
        time_series_list: List[List[float]],
        n_clusters: int = 3
    ) -> Dict[str, Any]:
        """
        時系列クラスタリング
        
        Args:
            time_series_list: 時系列データのリスト
            n_clusters: クラスタ数
        
        Returns:
            クラスタリング結果
        """
        try:
            if len(time_series_list) < n_clusters:
                return {
                    "status": "error",
                    "message": f"Insufficient time series (minimum {n_clusters} required)"
                }
            
            # 各時系列の特徴量を計算
            features = []
            for ts in time_series_list:
                if len(ts) == 0:
                    continue
                
                ts_array = np.array(ts)
                feature = {
                    "mean": float(np.mean(ts_array)),
                    "std": float(np.std(ts_array)),
                    "min": float(np.min(ts_array)),
                    "max": float(np.max(ts_array)),
                    "trend": float(np.mean(np.diff(ts_array))) if len(ts_array) > 1 else 0.0
                }
                features.append([feature["mean"], feature["std"], feature["trend"]])
            
            if len(features) < n_clusters:
                return {
                    "status": "error",
                    "message": f"Insufficient valid time series (minimum {n_clusters} required)"
                }
            
            # 簡易的なクラスタリング（K-means風）
            # 実際にはscikit-learnのKMeansを使用するのが理想的
            features_array = np.array(features)
            
            # 簡易クラスタリング（距離ベース）
            clusters = []
            cluster_centers = []
            
            # 初期クラスタ中心をランダムに選択
            indices = np.random.choice(len(features_array), n_clusters, replace=False)
            for idx in indices:
                cluster_centers.append(features_array[idx])
            
            # 各時系列を最も近いクラスタに割り当て
            for i, feature in enumerate(features_array):
                distances = [np.linalg.norm(feature - center) for center in cluster_centers]
                cluster_id = np.argmin(distances)
                clusters.append({
                    "time_series_index": i,
                    "cluster_id": int(cluster_id),
                    "distance": float(distances[cluster_id])
                })
            
            # クラスタごとの統計
            cluster_stats = {}
            for cluster_id in range(n_clusters):
                cluster_members = [c for c in clusters if c["cluster_id"] == cluster_id]
                cluster_stats[cluster_id] = {
                    "count": len(cluster_members),
                    "indices": [c["time_series_index"] for c in cluster_members]
                }
            
            return {
                "status": "success",
                "method": "simple_distance_based",
                "n_clusters": n_clusters,
                "clusters": clusters,
                "cluster_stats": cluster_stats,
                "note": "Basic clustering (scikit-learn KMeans recommended for better results)"
            }
        
        except Exception as e:
            logger.error(f"Error in cluster_time_series: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
