"""
金融・FinTechモジュール
既存のfintech_ai.pyと統合
"""
import logging
import sys
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# プロジェクトルート（ワークスペースルートを取得）
_current_file = Path(__file__).resolve()
PROJECT_ROOT = _current_file.parent.parent.parent.parent.parent

# デバッグ用: パスを確認
import logging
_logger = logging.getLogger(__name__)
_logger.debug(f"PROJECT_ROOT: {PROJECT_ROOT}")


class FinanceModule:
    """
    金融・FinTechモジュール
    
    機能:
    - 不正検知
    - リスク評価
    - 金融相談
    """
    
    def __init__(self):
        """初期化"""
        self.finance_service = None
        self._initialize_finance_service()
    
    def _initialize_finance_service(self):
        """既存の金融サービスを初期化"""
        try:
            # 既存のfintech_ai.pyを探す
            finance_paths = [
                PROJECT_ROOT / "次世代マルチモーダルAI統合プラットフォームv8.0" / "app" / "services" / "fintech_ai.py",
                PROJECT_ROOT / "極秘　優先順位1位　次世代エンタープライズAI統合プラットフォーム v3.0" / "app" / "services" / "fintech_ai.py",
            ]
            
            for path in finance_paths:
                logger.debug(f"金融サービスパスを確認: {path} (存在: {path.exists()})")
                if path.exists():
                    logger.info(f"金融サービスが見つかりました: {path}")
                    try:
                        # 動的にインポート
                        import importlib.util
                        spec = importlib.util.spec_from_file_location("fintech_ai", path)
                        fintech_module = importlib.util.module_from_spec(spec)
                        
                        # 依存関係のパスを追加
                        service_dir = path.parent
                        if str(service_dir) not in sys.path:
                            sys.path.insert(0, str(service_dir))
                        
                        spec.loader.exec_module(fintech_module)
                        
                        # FinTechAIServiceを取得
                        self.finance_service = fintech_module.FinTechAIService()
                        logger.info("金融サービスを初期化しました")
                        break
                    except Exception as e:
                        logger.warning(f"金融サービスのインポートに失敗: {e}")
                        continue
            
            if self.finance_service is None:
                logger.warning("金融サービスが見つかりませんでした。フォールバックモードで動作します。")
                logger.debug(f"確認したパス: {[str(p) for p in finance_paths]}")
        
        except Exception as e:
            logger.warning(f"金融サービスの初期化に失敗: {e}")
    
    def is_available(self) -> bool:
        """サービスが利用可能か"""
        return self.finance_service is not None
    
    def get_display_name(self) -> str:
        """表示名"""
        return "金融・FinTech"
    
    def get_description(self) -> str:
        """説明"""
        return "不正検知、リスク評価、金融相談"
    
    async def handle_query(self, question: str, connection_id: int = 0) -> str:
        """
        金融に関する質問を処理
        
        Args:
            question: 質問文
            connection_id: 接続ID
        
        Returns:
            応答テキスト
        """
        try:
            question_lower = question.lower()
            
            # リスク評価
            if any(keyword in question_lower for keyword in ["リスク", "信用", "評価", "スコア"]):
                return await self._handle_risk_assessment(question, connection_id)
            
            # 不正検知
            elif any(keyword in question_lower for keyword in ["不正", "検知", "異常", "詐欺"]):
                return await self._handle_fraud_detection(question)
            
            # ポートフォリオ最適化
            elif any(keyword in question_lower for keyword in ["ポートフォリオ", "投資", "最適化"]):
                return await self._handle_portfolio_optimization(question)
            
            # 金融相談
            elif any(keyword in question_lower for keyword in ["相談", "アドバイス", "推奨"]):
                return await self._handle_financial_consultation(question)
            
            # 既存システムと統合
            elif self.finance_service:
                # リスク評価を呼び出し
                if "リスク" in question_lower:
                    customer_data = {
                        "customer_id": f"user_{connection_id}",
                        "age": 30,
                        "income": 50000,
                        "credit_history_years": 5,
                        "debt_ratio": 0.3,
                        "employment_status": 1
                    }
                    result = self.finance_service.assess_credit_risk(customer_data)
                    
                    if result.get("status") == "success":
                        risk_score = result.get("risk_score", 0)
                        risk_level = result.get("risk_level", "unknown")
                        recommendation = result.get("recommendation", "")
                        return f"信用リスク評価結果:\n- リスクスコア: {risk_score:.2%}\n- リスクレベル: {risk_level}\n- 推奨: {recommendation}"
            
            # フォールバック: 簡易応答
            return f"金融に関する質問「{question}」について、専門家に相談することをお勧めします。"
        
        except Exception as e:
            logger.error(f"金融クエリ処理エラー: {e}")
            return f"エラーが発生しました: {str(e)}"
    
    async def _handle_risk_assessment(self, question: str, connection_id: int) -> str:
        """リスク評価を処理"""
        if self.finance_service:
            customer_data = {
                "customer_id": f"user_{connection_id}",
                "age": 30,
                "income": 50000,
                "credit_history_years": 5,
                "debt_ratio": 0.3,
                "employment_status": 1
            }
            result = self.finance_service.assess_credit_risk(customer_data)
            
            if result.get("status") == "success":
                risk_score = result.get("risk_score", 0)
                risk_level = result.get("risk_level", "unknown")
                recommendation = result.get("recommendation", "")
                return f"信用リスク評価:\n- リスクスコア: {risk_score:.2%}\n- リスクレベル: {risk_level}\n- 推奨: {recommendation}"
        
        return "リスク評価には顧客情報が必要です。詳しい情報を提供してください。"
    
    async def _handle_fraud_detection(self, question: str) -> str:
        """不正検知を処理"""
        if self.finance_service:
            transaction_data = {
                "amount": 1000,
                "time_of_day": 12,
                "merchant_category": 1,
                "location_distance": 0,
                "transaction_frequency": 1
            }
            result = self.finance_service.detect_fraud(transaction_data)
            
            if result.get("status") == "success":
                fraud_score = result.get("fraud_score", 0)
                is_fraud = result.get("is_fraud", False)
                return f"不正検知結果:\n- 不正スコア: {fraud_score:.2%}\n- 不正の可能性: {'あり' if is_fraud else '低い'}"
        
        return "不正検知には取引情報が必要です。"
    
    async def _handle_portfolio_optimization(self, question: str) -> str:
        """ポートフォリオ最適化を処理"""
        if self.finance_service:
            market_data = {
                "assets": [
                    {"name": "株式A", "return": 0.08, "risk": 0.15},
                    {"name": "債券B", "return": 0.04, "risk": 0.05},
                ]
            }
            result = self.finance_service.optimize_portfolio(market_data)
            
            if result.get("status") == "success":
                weights = result.get("weights", {})
                expected_return = result.get("expected_return", 0)
                return f"ポートフォリオ最適化結果:\n- 配分: {weights}\n- 期待リターン: {expected_return:.2%}"
        
        return "ポートフォリオ最適化には市場データが必要です。"
    
    async def _handle_financial_consultation(self, question: str) -> str:
        """金融相談を処理"""
        return "金融相談について、以下の分野でサポートできます:\n- 投資アドバイス\n- リスク管理\n- 資産運用\n- ローン相談\n\n詳しく知りたい項目を教えてください。"
