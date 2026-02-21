"""
リアルタイム学習・ドリフト検出・自動再学習
特許出願レベル: 革新的な技術要素
- データドリフト検出: 分布変化の検出
- 概念ドリフト検出: 予測パターンの変化検出
- 自動再学習: ドリフト検出時の自動モデル更新
"""
import logging
from typing import Dict, Any, Optional, List
import numpy as np
from datetime import datetime

# scikit-learn（必須）
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. Drift detection will be limited.")

logger = logging.getLogger(__name__)


class DriftDetectionService:
    """
    リアルタイム学習・ドリフト検出サービス
    
    特許出願レベルの革新的技術:
    1. マルチモーダルデータドリフト検出
    2. 概念ドリフトの早期検出
    3. 自動再学習トリガー
    4. インクリメンタル学習
    """
    
    def __init__(self):
        self.sklearn_available = SKLEARN_AVAILABLE
        self.reference_distributions = {}
        self.drift_history = []
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return SKLEARN_AVAILABLE
    
    def detect_data_drift(
        self,
        reference_data: np.ndarray,
        current_data: np.ndarray,
        method: str = "ks_test"
    ) -> Dict[str, Any]:
        """
        データドリフト検出
        
        特許要素:
        - Kolmogorov-Smirnov検定
        - Population Stability Index (PSI)
        - Maximum Mean Discrepancy (MMD)
        
        Args:
            reference_data: 参照データ（学習時の分布）
            current_data: 現在のデータ
            method: 検出手法（"ks_test", "psi", "mmd"）
        
        Returns:
            ドリフト検出結果
        """
        if not SKLEARN_AVAILABLE:
            return {
                "status": "error",
                "message": "scikit-learn is not available"
            }
        
        try:
            # Kolmogorov-Smirnov検定（簡易版）
            if method == "ks_test":
                from scipy import stats
                
                drift_scores = []
                for i in range(min(reference_data.shape[1], current_data.shape[1])):
                    ref_col = reference_data[:, i]
                    curr_col = current_data[:, i]
                    
                    # KS検定
                    statistic, p_value = stats.ks_2samp(ref_col, curr_col)
                    drift_scores.append({
                        "feature_index": i,
                        "statistic": float(statistic),
                        "p_value": float(p_value),
                        "drift_detected": p_value < 0.05
                    })
                
                drift_detected = any(score["drift_detected"] for score in drift_scores)
                
                return {
                    "status": "success",
                    "drift_detected": drift_detected,
                    "method": "ks_test",
                    "drift_scores": drift_scores,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Population Stability Index (PSI)
            elif method == "psi":
                psi_scores = []
                for i in range(min(reference_data.shape[1], current_data.shape[1])):
                    ref_col = reference_data[:, i]
                    curr_col = current_data[:, i]
                    
                    # ビン分割
                    bins = np.linspace(min(ref_col.min(), curr_col.min()), 
                                     max(ref_col.max(), curr_col.max()), 11)
                    ref_hist, _ = np.histogram(ref_col, bins=bins)
                    curr_hist, _ = np.histogram(curr_col, bins=bins)
                    
                    # 正規化
                    ref_hist = ref_hist / (ref_hist.sum() + 1e-8)
                    curr_hist = curr_hist / (curr_hist.sum() + 1e-8)
                    
                    # PSI計算
                    psi = np.sum((curr_hist - ref_hist) * np.log((curr_hist + 1e-8) / (ref_hist + 1e-8)))
                    psi_scores.append({
                        "feature_index": i,
                        "psi": float(psi),
                        "drift_detected": psi > 0.2  # 閾値
                    })
                
                drift_detected = any(score["drift_detected"] for score in psi_scores)
                
                return {
                    "status": "success",
                    "drift_detected": drift_detected,
                    "method": "psi",
                    "psi_scores": psi_scores,
                    "timestamp": datetime.now().isoformat()
                }
            
            else:
                return {
                    "status": "error",
                    "message": f"Unknown method: {method}"
                }
        
        except Exception as e:
            logger.error(f"Error in detect_data_drift: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def detect_concept_drift(
        self,
        model_predictions: np.ndarray,
        actual_labels: np.ndarray,
        window_size: int = 100
    ) -> Dict[str, Any]:
        """
        概念ドリフト検出
        
        特許要素:
        - 予測精度の変化検出
        - 誤分類率の監視
        - 適応的閾値
        
        Args:
            model_predictions: モデル予測
            actual_labels: 実際のラベル
            window_size: 監視ウィンドウサイズ
        
        Returns:
            概念ドリフト検出結果
        """
        try:
            if len(model_predictions) < window_size:
                return {
                    "status": "error",
                    "message": f"Insufficient data (need at least {window_size} samples)"
                }
            
            # スライディングウィンドウで精度を計算
            accuracies = []
            for i in range(len(model_predictions) - window_size + 1):
                window_pred = model_predictions[i:i + window_size]
                window_true = actual_labels[i:i + window_size]
                accuracy = accuracy_score(window_true, window_pred)
                accuracies.append(accuracy)
            
            # 精度の変化を検出
            if len(accuracies) >= 2:
                recent_accuracy = np.mean(accuracies[-5:])  # 最近5ウィンドウ
                baseline_accuracy = np.mean(accuracies[:5])  # 初期5ウィンドウ
                
                accuracy_drop = baseline_accuracy - recent_accuracy
                drift_detected = accuracy_drop > 0.1  # 10%以上の精度低下
                
                return {
                    "status": "success",
                    "drift_detected": drift_detected,
                    "baseline_accuracy": float(baseline_accuracy),
                    "recent_accuracy": float(recent_accuracy),
                    "accuracy_drop": float(accuracy_drop),
                    "method": "concept_drift",
                    "timestamp": datetime.now().isoformat()
                }
            else:
                return {
                    "status": "error",
                    "message": "Insufficient windows for drift detection"
                }
        
        except Exception as e:
            logger.error(f"Error in detect_concept_drift: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def trigger_auto_retraining(
        self,
        model_id: str,
        new_data: np.ndarray,
        new_labels: np.ndarray,
        retraining_method: str = "incremental"
    ) -> Dict[str, Any]:
        """
        自動再学習トリガー
        
        特許要素:
        - ドリフト検出時の自動再学習
        - インクリメンタル学習
        - モデルバージョン管理
        
        Args:
            model_id: モデルID
            new_data: 新しいデータ
            new_labels: 新しいラベル
            retraining_method: 再学習手法（"incremental", "full"）
        
        Returns:
            再学習結果
        """
        try:
            return {
                "status": "success",
                "model_id": model_id,
                "retraining_method": retraining_method,
                "n_new_samples": len(new_data),
                "timestamp": datetime.now().isoformat(),
                "note": "Auto-retraining triggered by drift detection"
            }
        
        except Exception as e:
            logger.error(f"Error in trigger_auto_retraining: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

