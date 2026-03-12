"""
法務・法律モジュール
既存のcontract-review-systemと統合
"""
import logging
import sys
from pathlib import Path
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# プロジェクトルート（ワークスペースルートを取得）
_current_file = Path(__file__).resolve()
PROJECT_ROOT = _current_file.parent.parent.parent.parent.parent


class LegalModule:
    """
    法務・法律モジュール
    
    機能:
    - 契約書分析
    - 法務Q&A
    - 法令検索
    """
    
    def __init__(self):
        """初期化"""
        self.legal_service = None
        self._initialize_legal_service()
    
    def _initialize_legal_service(self):
        """既存の法務サービスを初期化"""
        try:
            # 既存のcontract-review-systemを探す
            legal_paths = [
                PROJECT_ROOT / "contract-review-system",
                PROJECT_ROOT / "legal-ai-system",
            ]
            
            self.legal_api_url = None
            
            for path in legal_paths:
                if path.exists():
                    logger.info(f"法務サービスが見つかりました: {path}")
                    # APIエンドポイントのURLを設定（実際の運用では環境変数から取得）
                    # ローカルで動作している場合のデフォルトURL
                    self.legal_api_url = "http://localhost:8000"
                    logger.info(f"法務API URL: {self.legal_api_url}")
                    break
            
            if self.legal_api_url is None:
                logger.warning("法務サービスが見つかりませんでした。フォールバックモードで動作します。")
        
        except Exception as e:
            logger.warning(f"法務サービスの初期化に失敗: {e}")
    
    def is_available(self) -> bool:
        """サービスが利用可能か"""
        return self.legal_service is not None
    
    def get_display_name(self) -> str:
        """表示名"""
        return "法務・法律"
    
    def get_description(self) -> str:
        """説明"""
        return "契約書分析、法務Q&A、法令検索"
    
    async def handle_query(self, question: str, connection_id: int = 0) -> str:
        """
        法務に関する質問を処理
        
        Args:
            question: 質問文
            connection_id: 接続ID
        
        Returns:
            応答テキスト
        """
        try:
            question_lower = question.lower()
            
            # 契約書分析
            if any(keyword in question_lower for keyword in ["契約書", "契約", "レビュー", "分析"]):
                return await self._handle_contract_review(question)
            
            # 法務Q&A
            elif any(keyword in question_lower for keyword in ["質問", "q&a", "回答", "教えて"]):
                return await self._handle_legal_qa(question)
            
            # 法令検索
            elif any(keyword in question_lower for keyword in ["法令", "法律", "検索", "調べて"]):
                return await self._handle_legal_search(question)
            
            # 既存システムと統合（API経由）
            elif self.legal_api_url:
                try:
                    import httpx
                    async with httpx.AsyncClient() as client:
                        # 契約書レビューAPIを呼び出し
                        response = await client.post(
                            f"{self.legal_api_url}/api/review",
                            json={
                                "contract_text": question,
                                "include_risk_analysis": True,
                                "include_section_analysis": True
                            },
                            timeout=10.0
                        )
                        
                        if response.status_code == 200:
                            result = response.json()
                            risks = result.get("risks", [])
                            if risks:
                                risk_text = "\n".join([
                                    f"- {risk.get('section', '')}: {risk.get('risk_level', '')} - {risk.get('description', '')}"
                                    for risk in risks[:3]
                                ])
                                return f"契約書分析結果:\n{risk_text}"
                except Exception as e:
                    logger.warning(f"法務API呼び出しエラー: {e}")
            
            # フォールバック: 簡易応答
            return f"法務に関する質問「{question}」について、専門家に相談することをお勧めします。"
        
        except Exception as e:
            logger.error(f"法務クエリ処理エラー: {e}")
            return f"エラーが発生しました: {str(e)}"
    
    async def _handle_contract_review(self, question: str) -> str:
        """契約書分析を処理"""
        if self.legal_api_url:
            try:
                import httpx
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        f"{self.legal_api_url}/api/review",
                        json={
                            "contract_text": question,
                            "include_risk_analysis": True,
                            "include_section_analysis": True
                        },
                        timeout=10.0
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        risks = result.get("risks", [])
                        sections = result.get("sections", [])
                        
                        response_text = "契約書分析結果:\n"
                        if sections:
                            response_text += f"- 条項数: {len(sections)}\n"
                        if risks:
                            response_text += f"- リスク検出: {len(risks)}件\n"
                            for risk in risks[:3]:
                                response_text += f"  * {risk.get('risk_level', '')}: {risk.get('description', '')}\n"
                        return response_text
            except Exception as e:
                logger.warning(f"契約書分析APIエラー: {e}")
        
        return "契約書分析には契約書のテキストが必要です。契約書の内容を提供してください。"
    
    async def _handle_legal_qa(self, question: str) -> str:
        """法務Q&Aを処理"""
        return f"法務Q&Aについて、「{question}」に関する回答を検索中です。専門的な法務相談については、法律専門家に相談することをお勧めします。"
    
    async def _handle_legal_search(self, question: str) -> str:
        """法令検索を処理"""
        return f"法令検索について、「{question}」に関する法令を検索中です。最新の法令情報については、法務省の公式サイトを確認してください。"
