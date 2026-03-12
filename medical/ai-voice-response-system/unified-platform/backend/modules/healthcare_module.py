"""
医療・ヘルスケアモジュール
既存のhealthcare_ai.pyと統合
"""
import logging
import sys
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# プロジェクトルート（ワークスペースルートを取得）
# unified-platform/backend/modules/healthcare_module.py から
# ワークスペースルートまで: ../../../
_current_file = Path(__file__).resolve()
# ai-voice-response-system/unified-platform/backend/modules/healthcare_module.py
# -> ai-voice-response-system/unified-platform/backend/modules (parent)
# -> ai-voice-response-system/unified-platform/backend (parent.parent)
# -> ai-voice-response-system/unified-platform (parent.parent.parent)
# -> ai-voice-response-system (parent.parent.parent.parent)
# -> ワークスペースルート (parent.parent.parent.parent.parent)
PROJECT_ROOT = _current_file.parent.parent.parent.parent.parent

# デバッグ用: パスを確認
import logging
_logger = logging.getLogger(__name__)
_logger.debug(f"PROJECT_ROOT: {PROJECT_ROOT}")


class HealthcareModule:
    """
    医療・ヘルスケアモジュール
    
    機能:
    - 症状相談
    - 健康管理
    - 医療情報検索
    """
    
    def __init__(self):
        """初期化"""
        self.healthcare_service = None
        self._initialize_healthcare_service()
    
    def _initialize_healthcare_service(self):
        """既存の医療サービスを初期化"""
        try:
            # 既存のhealthcare_ai.pyを探す
            healthcare_paths = [
                PROJECT_ROOT / "次世代マルチモーダルAI統合プラットフォームv8.0" / "app" / "services" / "healthcare_ai.py",
                PROJECT_ROOT / "極秘　優先順位1位　次世代エンタープライズAI統合プラットフォーム v3.0" / "app" / "services" / "healthcare_ai.py",
            ]
            
            for path in healthcare_paths:
                logger.debug(f"医療サービスパスを確認: {path} (存在: {path.exists()})")
                if path.exists():
                    logger.info(f"医療サービスが見つかりました: {path}")
                    try:
                        # 動的にインポート
                        import importlib.util
                        spec = importlib.util.spec_from_file_location("healthcare_ai", path)
                        healthcare_module = importlib.util.module_from_spec(spec)
                        
                        # 依存関係のパスを追加
                        service_dir = path.parent
                        if str(service_dir) not in sys.path:
                            sys.path.insert(0, str(service_dir))
                        
                        spec.loader.exec_module(healthcare_module)
                        
                        # HealthcareAIServiceを取得
                        self.healthcare_service = healthcare_module.HealthcareAIService()
                        logger.info("医療サービスを初期化しました")
                        break
                    except Exception as e:
                        logger.warning(f"医療サービスのインポートに失敗: {e}")
                        continue
            
            if self.healthcare_service is None:
                logger.warning("医療サービスが見つかりませんでした。フォールバックモードで動作します。")
                logger.debug(f"確認したパス: {[str(p) for p in healthcare_paths]}")
        
        except Exception as e:
            logger.warning(f"医療サービスの初期化に失敗: {e}")
    
    def is_available(self) -> bool:
        """サービスが利用可能か"""
        return self.healthcare_service is not None
    
    def get_display_name(self) -> str:
        """表示名"""
        return "医療・ヘルスケア"
    
    def get_description(self) -> str:
        """説明"""
        return "症状相談、健康管理、医療情報検索"
    
    async def handle_query(self, question: str, connection_id: int = 0) -> str:
        """
        医療に関する質問を処理
        
        Args:
            question: 質問文
            connection_id: 接続ID
        
        Returns:
            応答テキスト
        """
        try:
            question_lower = question.lower()
            
            # 症状相談
            if any(keyword in question_lower for keyword in ["症状", "痛み", "頭痛", "発熱", "咳", "疲労"]):
                return await self._handle_symptom_consultation(question)
            
            # 健康管理
            elif any(keyword in question_lower for keyword in ["健康", "管理", "体重", "血圧", "運動"]):
                return await self._handle_health_management(question)
            
            # 医療情報検索
            elif any(keyword in question_lower for keyword in ["検索", "情報", "病気", "疾患", "治療"]):
                return await self._handle_medical_search(question)
            
            # 既存システムと統合
            elif self.healthcare_service:
                # 診断支援を呼び出し
                symptoms = self._extract_symptoms(question)
                if symptoms:
                    patient_data = {"patient_id": f"user_{connection_id}"}
                    result = self.healthcare_service.support_diagnosis(patient_data, symptoms)
                    
                    if result.get("status") == "success":
                        recommendations = result.get("recommendations", [])
                        if recommendations:
                            response = "診断支援の結果:\n"
                            for rec in recommendations[:3]:
                                disease = rec.get("disease", "")
                                prob = rec.get("probability", 0)
                                tests = rec.get("recommended_tests", [])
                                response += f"- {disease} (可能性: {prob:.1%})\n"
                                if tests:
                                    response += f"  推奨検査: {', '.join(tests)}\n"
                            return response
            
            # フォールバック: 簡易応答
            return f"医療に関する質問「{question}」について、専門家に相談することをお勧めします。"
        
        except Exception as e:
            logger.error(f"医療クエリ処理エラー: {e}")
            return f"エラーが発生しました: {str(e)}"
    
    def _extract_symptoms(self, text: str) -> list:
        """症状を抽出"""
        symptoms = []
        symptom_keywords = {
            "頭痛": "headache",
            "発熱": "fever",
            "咳": "cough",
            "疲労": "fatigue",
            "腹痛": "abdominal_pain",
            "めまい": "dizziness"
        }
        
        for keyword, symptom in symptom_keywords.items():
            if keyword in text:
                symptoms.append(symptom)
        
        return symptoms
    
    async def _handle_symptom_consultation(self, question: str) -> str:
        """症状相談を処理"""
        if self.healthcare_service:
            symptoms = self._extract_symptoms(question)
            if symptoms:
                patient_data = {"patient_id": "user"}
                result = self.healthcare_service.support_diagnosis(patient_data, symptoms)
                
                if result.get("status") == "success":
                    recommendations = result.get("recommendations", [])
                    if recommendations:
                        response = "症状相談の結果:\n"
                        for rec in recommendations[:3]:
                            disease = rec.get("disease", "")
                            prob = rec.get("probability", 0)
                            response += f"- {disease} (可能性: {prob:.1%})\n"
                        response += "\n※専門医の診断を受けることをお勧めします。"
                        return response
        
        return "症状について詳しく教えていただけますか？専門家に相談することをお勧めします。"
    
    async def _handle_health_management(self, question: str) -> str:
        """健康管理を処理"""
        return "健康管理について、以下の情報を提供できます:\n- 体重管理\n- 血圧管理\n- 運動記録\n- 食事記録\n\n詳しく知りたい項目を教えてください。"
    
    async def _handle_medical_search(self, question: str) -> str:
        """医療情報検索を処理"""
        return f"医療情報「{question}」を検索中です。専門的な医療情報については、医療機関に相談することをお勧めします。"
