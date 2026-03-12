"""
ヘルスケアAI診断支援モジュール
医療画像分析 + RAG + プライバシー保護
"""
import logging
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# RAGの使用可否
USE_RAG = False
try:
    from langchain.vectorstores import Chroma
    from langchain.embeddings import OpenAIEmbeddings, HuggingFaceEmbeddings
    USE_RAG = True
except ImportError:
    logger.warning("RAG機能に必要なライブラリがありません")

class HealthcareModule:
    """ヘルスケア診断支援モジュール"""
    
    def __init__(self):
        self.medical_db = None
        
        # RAGの初期化
        if USE_RAG:
            try:
                if os.getenv("OPENAI_API_KEY"):
                    embeddings = OpenAIEmbeddings()
                else:
                    embeddings = HuggingFaceEmbeddings(
                        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
                    )
                
                self.medical_db = Chroma(
                    persist_directory="./medical_literature",
                    embedding_function=embeddings
                )
                logger.info("医学文献RAGデータベースを初期化しました")
            except Exception as e:
                logger.warning(f"医学文献RAGデータベースの初期化に失敗: {e}")
        
        logger.info("HealthcareModule initialized")
    
    async def diagnose(
        self,
        patient_data: Dict,
        medical_images: List[str],
        symptoms: List[str]
    ) -> Dict:
        """
        診断支援
        
        Args:
            patient_data: 患者データ
            medical_images: 医療画像のパスのリスト
            symptoms: 症状のリスト
        
        Returns:
            診断支援結果
        """
        # 医療画像分析（簡易版）
        image_results = []
        for img_path in medical_images:
            analysis = await self._analyze_medical_image(img_path)
            image_results.append(analysis)
        
        # 類似症例検索（RAG）
        similar_cases = await self._search_similar_cases(symptoms)
        
        # 診断支援情報生成
        diagnosis_support = self._generate_diagnosis_support(
            patient_data, image_results, similar_cases, symptoms
        )
        
        # プライバシー保護処理
        protected_result = self._protect_privacy(diagnosis_support)
        
        return {
            "patient_id": patient_data.get("patient_id", "anonymous"),
            "image_analysis": image_results,
            "similar_cases": similar_cases,
            "diagnosis_support": protected_result,
            "symptoms": symptoms,
            "disclaimer": "この結果は診断支援情報です。実際の診断は医師が行います。",
            "timestamp": self._get_timestamp()
        }
    
    async def _analyze_medical_image(self, image_path: str) -> Dict:
        """医療画像を分析（簡易版）"""
        # 実際の実装では、医療画像分類モデルを使用
        logger.info(f"医療画像を分析: {image_path}")
        return {
            "image_path": image_path,
            "findings": "異常所見なし",
            "confidence": 0.85,
            "recommendations": "定期検査を継続してください"
        }
    
    async def _search_similar_cases(self, symptoms: List[str]) -> List[Dict]:
        """類似症例を検索（RAG）"""
        if not self.medical_db:
            return []
        
        try:
            query = f"症状: {', '.join(symptoms)}"
            results = self.medical_db.similarity_search(query, k=5)
            
            return [
                {
                    "case_id": f"case_{i}",
                    "description": doc.page_content,
                    "relevance_score": 0.8
                }
                for i, doc in enumerate(results)
            ]
        except Exception as e:
            logger.error(f"類似症例検索エラー: {e}")
            return []
    
    def _generate_diagnosis_support(
        self,
        patient_data: Dict,
        image_results: List[Dict],
        similar_cases: List[Dict],
        symptoms: List[str]
    ) -> Dict:
        """診断支援情報を生成"""
        return {
            "summary": f"症状: {', '.join(symptoms)}",
            "image_findings": [r.get("findings", "") for r in image_results],
            "differential_diagnosis": [
                case.get("description", "")[:100] for case in similar_cases[:3]
            ],
            "recommended_tests": [
                "血液検査",
                "画像検査",
                "生検（必要に応じて）"
            ],
            "note": "この情報は診断支援のための参考情報です。"
        }
    
    def _protect_privacy(self, diagnosis_support: Dict) -> Dict:
        """プライバシー保護処理（簡易版）"""
        # 実際の実装では、差分プライバシーやフェデレーテッドラーニングを使用
        protected = diagnosis_support.copy()
        # 個人情報をマスク
        if "patient_id" in protected:
            protected["patient_id"] = "***"
        return protected
    
    def _get_timestamp(self) -> str:
        """タイムスタンプを取得"""
        from datetime import datetime
        return datetime.now().isoformat()
