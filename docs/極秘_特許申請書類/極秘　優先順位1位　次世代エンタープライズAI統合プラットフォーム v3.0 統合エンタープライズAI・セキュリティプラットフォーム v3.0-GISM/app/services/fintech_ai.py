"""
金融AI（FinTech）サービス
フェーズ4: ドメイン特化統合
- リスク評価: 信用スコアリング、デフォルト予測
- アルゴリズム取引: 時系列予測、ポートフォリオ最適化
- 不正検知: 異常検知、マネーロンダリング検知
"""
import logging
from typing import Dict, Any, Optional, List
import numpy as np

# scikit-learn（リスク評価、不正検知、必須）
try:
    from sklearn.ensemble import RandomForestClassifier, IsolationForest
    from sklearn.preprocessing import StandardScaler
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logging.warning("scikit-learn not available. FinTech AI functionality will be limited.")

# scipy（最適化、必須）
try:
    from scipy.optimize import minimize
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False
    logging.warning("scipy not available. Portfolio optimization will be limited.")

logger = logging.getLogger(__name__)


class FinTechAIService:
    """金融AI（FinTech）サービス"""
    
    def __init__(self):
        self.sklearn_available = SKLEARN_AVAILABLE
        self.scipy_available = SCIPY_AVAILABLE
        self.risk_model = None
        self.fraud_detector = None
    
    def is_available(self) -> bool:
        """サービスが利用可能かチェック"""
        return SKLEARN_AVAILABLE and SCIPY_AVAILABLE
    
    def assess_credit_risk(self, customer_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        信用リスク評価
        
        Args:
            customer_data: 顧客データ
        
        Returns:
            リスク評価結果
        """
        if not SKLEARN_AVAILABLE:
            return {
                "status": "error",
                "message": "scikit-learn is not available"
            }
        
        try:
            # 特徴量を抽出
            features = [
                customer_data.get("age", 30),
                customer_data.get("income", 50000),
                customer_data.get("credit_history_years", 5),
                customer_data.get("debt_ratio", 0.3),
                customer_data.get("employment_status", 1)  # 1: employed, 0: unemployed
            ]
            
            # 簡易的なリスクスコア計算（実際には機械学習モデルを使用）
            # 年齢、収入、信用履歴、負債比率、雇用状況からリスクを計算
            age_score = 1.0 if features[0] >= 25 and features[0] <= 65 else 0.5
            income_score = min(features[1] / 100000, 1.0)  # 正規化
            credit_score = min(features[2] / 10, 1.0)  # 正規化
            debt_score = 1.0 - min(features[3], 1.0)  # 負債比率が低いほど良い
            employment_score = features[4]
            
            # 総合リスクスコア（0-1、低いほどリスクが高い）
            risk_score = (age_score * 0.1 + income_score * 0.3 + credit_score * 0.3 + 
                         debt_score * 0.2 + employment_score * 0.1)
            
            # リスクレベル判定
            if risk_score >= 0.7:
                risk_level = "low"
            elif risk_score >= 0.4:
                risk_level = "medium"
            else:
                risk_level = "high"
            
            return {
                "status": "success",
                "customer_id": customer_data.get("customer_id", "unknown"),
                "risk_score": float(risk_score),
                "risk_level": risk_level,
                "recommendation": "approve" if risk_level == "low" else "review",
                "note": "Basic risk assessment (ML model recommended for production)"
            }
        
        except Exception as e:
            logger.error(f"Error in assess_credit_risk: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def optimize_portfolio(
        self,
        market_data: Dict[str, Any],
        constraints: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        ポートフォリオ最適化
        
        Args:
            market_data: 市場データ（各資産のリターン、リスク）
            constraints: 制約条件
        
        Returns:
            最適化結果
        """
        if not SCIPY_AVAILABLE:
            return {
                "status": "error",
                "message": "scipy is not available"
            }
        
        try:
            # 資産のリターンとリスクを取得
            assets = market_data.get("assets", [])
            if len(assets) == 0:
                return {
                    "status": "error",
                    "message": "No assets provided"
                }
            
            # 簡易的なポートフォリオ最適化（等ウェイト）
            n_assets = len(assets)
            weights = [1.0 / n_assets] * n_assets
            
            # 期待リターンとリスクを計算
            expected_return = sum(asset.get("return", 0.05) * w for asset, w in zip(assets, weights))
            portfolio_risk = np.sqrt(sum(asset.get("risk", 0.1) ** 2 * w for asset, w in zip(assets, weights)))
            
            return {
                "status": "success",
                "weights": {asset.get("name", f"asset_{i}"): float(w) for i, (asset, w) in enumerate(zip(assets, weights))},
                "expected_return": float(expected_return),
                "portfolio_risk": float(portfolio_risk),
                "sharpe_ratio": float(expected_return / portfolio_risk) if portfolio_risk > 0 else 0.0,
                "method": "equal_weight",
                "note": "Basic portfolio optimization (Advanced optimization requires covariance matrix)"
            }
        
        except Exception as e:
            logger.error(f"Error in optimize_portfolio: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def detect_fraud(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        不正検知
        
        Args:
            transaction_data: 取引データ
        
        Returns:
            不正検知結果
        """
        if not SKLEARN_AVAILABLE:
            return {
                "status": "error",
                "message": "scikit-learn is not available"
            }
        
        try:
            # 特徴量を抽出
            features = [
                transaction_data.get("amount", 0),
                transaction_data.get("time_of_day", 12),
                transaction_data.get("merchant_category", 0),
                transaction_data.get("location_distance", 0),
                transaction_data.get("transaction_frequency", 1)
            ]
            
            # 簡易的な不正検知（ルールベース）
            fraud_score = 0.0
            
            # 金額が異常に大きい
            if features[0] > 10000:
                fraud_score += 0.3
            
            # 深夜の取引
            if features[1] < 6 or features[1] > 22:
                fraud_score += 0.2
            
            # 通常と異なる場所
            if features[3] > 100:  # 100km以上離れた場所
                fraud_score += 0.3
            
            # 異常に高い取引頻度
            if features[4] > 10:  # 1日10回以上
                fraud_score += 0.2
            
            is_fraud = fraud_score > 0.5
            
            return {
                "status": "success",
                "transaction_id": transaction_data.get("transaction_id", "unknown"),
                "is_fraud": is_fraud,
                "fraud_score": float(fraud_score),
                "risk_level": "high" if is_fraud else "low",
                "note": "Basic fraud detection (ML model recommended for production)"
            }
        
        except Exception as e:
            logger.error(f"Error in detect_fraud: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
    
    def predict_market_trends(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        市場トレンド予測
        
        Args:
            market_data: 市場データ（価格履歴等）
        
        Returns:
            予測結果
        """
        try:
            # 価格履歴を取得
            price_history = market_data.get("price_history", [])
            
            if len(price_history) < 10:
                return {
                    "status": "error",
                    "message": "Insufficient price history (minimum 10 data points required)"
                }
            
            # 簡易的なトレンド予測（移動平均）
            prices = np.array(price_history)
            short_ma = np.mean(prices[-5:])  # 短期移動平均
            long_ma = np.mean(prices[-10:])  # 長期移動平均
            
            trend = "upward" if short_ma > long_ma else "downward"
            momentum = (short_ma - long_ma) / long_ma if long_ma > 0 else 0.0
            
            return {
                "status": "success",
                "trend": trend,
                "momentum": float(momentum),
                "short_ma": float(short_ma),
                "long_ma": float(long_ma),
                "prediction": "buy" if trend == "upward" else "sell",
                "note": "Basic trend prediction (Advanced ML models recommended)"
            }
        
        except Exception as e:
            logger.error(f"Error in predict_market_trends: {e}")
            return {
                "status": "error",
                "message": str(e)
            }

