"""
既存システムと統合した面談支援サービス
"""
import os
import logging
from pathlib import Path
from typing import Dict, Optional, List
import re

from .interview_response_service import InterviewResponseService

logger = logging.getLogger(__name__)

# プロジェクトルートのパス
PROJECT_ROOT = Path(__file__).parent.parent.parent


class IntegratedInterviewService:
    """
    既存システムと統合した面談支援サービス
    
    機能:
    - 既存の面談準備資料の自動読み込み
    - 質問事項リストの活用
    - デモンストレーション準備との連携
    - 業界用語集の活用
    """
    
    def __init__(self):
        self.interview_service = InterviewResponseService()
        self.preparation_data = {}
        self.question_lists = []
        self.demo_data = {}
        self.industry_terms = {}
        self.company_name = None
    
    def load_all_preparation_data(self, company_name: str) -> Dict:
        """
        すべての準備資料を読み込む
        
        Args:
            company_name: 企業名（例: "AIexe", "Fusic"）
        
        Returns:
            読み込み結果
        """
        self.company_name = company_name
        results = {
            "company_info": {},
            "questions": [],
            "answers": [],
            "demo_data": {},
            "industry_terms": {}
        }
        
        try:
            # 1. 企業情報を読み込む
            company_info = self._load_company_info(company_name)
            if company_info:
                results["company_info"] = company_info
                self.interview_service.set_company_info(company_info)
            
            # 2. 質問事項リストを読み込む
            questions = self._load_question_list(company_name)
            if questions:
                results["questions"] = questions
                self.question_lists = questions
            
            # 3. 回答例を読み込む
            answers = self._load_answer_examples(company_name)
            if answers:
                results["answers"] = answers
            
            # 4. デモンストレーション準備を読み込む
            demo_data = self._load_demo_preparation(company_name)
            if demo_data:
                results["demo_data"] = demo_data
                self.demo_data = demo_data
            
            # 5. 業界用語集を読み込む
            industry_terms = self._load_industry_terms(company_name)
            if industry_terms:
                results["industry_terms"] = industry_terms
                self.industry_terms = industry_terms
            
            # 6. 候補者情報を構築
            candidate_info = self._build_candidate_info()
            if candidate_info:
                self.interview_service.set_candidate_info(candidate_info)
            
            logger.info(f"{company_name}の準備資料を読み込みました")
            return results
        
        except Exception as e:
            logger.error(f"準備資料の読み込みエラー: {e}")
            return results
    
    def _load_company_info(self, company_name: str) -> Optional[Dict]:
        """企業情報を読み込む"""
        try:
            # AIexeの場合
            if company_name == "AIexe":
                file_path = PROJECT_ROOT / "government-ai-security-platform" / "AIexe-面談準備ガイド.md"
                if file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                    
                    # 企業情報を抽出
                    company_info = {
                        "name": "AIexe株式会社",
                        "industry": "AI・機械学習",
                        "business": self._extract_value(content, "事業内容", "AI技術を活用したWebアプリケーション開発"),
                        "values": self._extract_value(content, "企業理念", "技術革新とチームワーク"),
                        "culture": "フルリモート、裁量労働制",
                    }
                    
                    # 面接官情報を抽出
                    interviewer_match = re.search(r"面談担当[：:]\s*(.+?)\s*\n", content)
                    if interviewer_match:
                        company_info["interviewer_name"] = interviewer_match.group(1).strip()
                    
                    return company_info
            
            # その他の企業も同様に処理可能
            return None
        
        except Exception as e:
            logger.error(f"企業情報の読み込みエラー: {e}")
            return None
    
    def _load_question_list(self, company_name: str) -> List[str]:
        """質問事項リストを読み込む"""
        try:
            questions = []
            
            # AIexeの場合
            if company_name == "AIexe":
                file_path = PROJECT_ROOT / "government-ai-security-platform" / "AIexe-質問事項リスト_面談用最終版.md"
                if file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                    
                    # Markdownから質問を抽出
                    for line in content.split('\n'):
                        # チェックボックス形式の質問を抽出
                        if re.match(r'^-\s*\[.*\]\s*(.+[？?])', line):
                            question = re.sub(r'^-\s*\[.*\]\s*', '', line).strip()
                            if question:
                                questions.append(question)
                        # 通常のリスト形式の質問を抽出
                        elif re.match(r'^[-*]\s*(.+[？?])', line):
                            question = re.sub(r'^[-*]\s*', '', line).strip()
                            if question:
                                questions.append(question)
            
            # 汎用の質問事項リストも読み込む
            generic_file = PROJECT_ROOT / "面談質問事項リスト_汎用版_20251207.md"
            if generic_file.exists():
                content = generic_file.read_text(encoding='utf-8')
                for line in content.split('\n'):
                    if re.match(r'^[-*]\s*(.+[？?])', line):
                        question = re.sub(r'^[-*]\s*', '', line).strip()
                        if question and question not in questions:
                            questions.append(question)
            
            return questions
        
        except Exception as e:
            logger.error(f"質問事項リストの読み込みエラー: {e}")
            return []
    
    def _load_answer_examples(self, company_name: str) -> List[Dict]:
        """回答例を読み込む"""
        try:
            answers = []
            
            # AIexeの場合
            if company_name == "AIexe":
                file_path = PROJECT_ROOT / "government-ai-security-platform" / "AIexe-30分面談-質問例と回答例.md"
                if file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                    
                    # Q&A形式を抽出
                    qa_pattern = r'###\s*(.+?)\n\n(.+?)(?=\n###|\Z)'
                    matches = re.finditer(qa_pattern, content, re.DOTALL)
                    
                    for match in matches:
                        question = match.group(1).strip()
                        answer = match.group(2).strip()
                        if question and answer:
                            answers.append({
                                "question": question,
                                "answer": answer
                            })
            
            return answers
        
        except Exception as e:
            logger.error(f"回答例の読み込みエラー: {e}")
            return []
    
    def _load_demo_preparation(self, company_name: str) -> Optional[Dict]:
        """デモンストレーション準備を読み込む"""
        try:
            demo_data = {
                "tech_stack": [],
                "achievements": []
            }
            
            # デモンストレーション準備ガイドを読み込む
            file_path = PROJECT_ROOT / "government-ai-security-platform" / "AIexe-デモンストレーション準備ガイド.md"
            if file_path.exists():
                content = file_path.read_text(encoding='utf-8')
                
                # 技術スタックを抽出
                tech_keywords = ["Python", "FastAPI", "React", "TypeScript", "LLM", "RAG", "LangChain", "ChromaDB"]
                for keyword in tech_keywords:
                    if keyword in content:
                        demo_data["tech_stack"].append(keyword)
                
                # 実績を抽出
                achievement_pattern = r'(?:実績|実装|開発).*?[:：]\s*(.+?)(?=\n|$)'
                matches = re.finditer(achievement_pattern, content, re.MULTILINE)
                for match in matches:
                    achievement = match.group(1).strip()
                    if achievement:
                        demo_data["achievements"].append(achievement)
            
            return demo_data if demo_data["tech_stack"] or demo_data["achievements"] else None
        
        except Exception as e:
            logger.error(f"デモンストレーション準備の読み込みエラー: {e}")
            return None
    
    def _load_industry_terms(self, company_name: str) -> Dict[str, str]:
        """業界用語集を読み込む"""
        try:
            terms = {}
            
            # AIexeの場合
            if company_name == "AIexe":
                file_path = PROJECT_ROOT / "government-ai-security-platform" / "AIexe-面談用_業界用語集.md"
                if file_path.exists():
                    content = file_path.read_text(encoding='utf-8')
                    
                    # CSV形式またはMarkdown形式から用語を抽出
                    for line in content.split('\n'):
                        # CSV形式: "LLM,大規模言語モデル"
                        if ',' in line:
                            parts = line.split(',')
                            if len(parts) >= 2:
                                term = parts[0].strip()
                                definition = parts[1].strip()
                                if term and definition:
                                    terms[term] = definition
                        # Markdown形式: "- **LLM**: 大規模言語モデル"
                        elif re.match(r'^[-*]\s*\*\*(.+?)\*\*[:：]\s*(.+)$', line):
                            match = re.match(r'^[-*]\s*\*\*(.+?)\*\*[:：]\s*(.+)$', line)
                            if match:
                                term = match.group(1).strip()
                                definition = match.group(2).strip()
                                if term and definition:
                                    terms[term] = definition
            
            return terms
        
        except Exception as e:
            logger.error(f"業界用語集の読み込みエラー: {e}")
            return {}
    
    def _build_candidate_info(self) -> Optional[Dict]:
        """デモンストレーション準備から候補者情報を構築"""
        try:
            candidate_info = {}
            
            # デモンストレーション準備から技術スタックを取得
            if self.demo_data.get("tech_stack"):
                candidate_info["skills"] = self.demo_data["tech_stack"]
            
            # 実績をフォーマット
            if self.demo_data.get("achievements"):
                candidate_info["experience"] = "\n".join(self.demo_data["achievements"])
            
            return candidate_info if candidate_info else None
        
        except Exception as e:
            logger.error(f"候補者情報の構築エラー: {e}")
            return None
    
    def _extract_value(self, content: str, key: str, default: str = "") -> str:
        """コンテンツから値を抽出"""
        pattern = rf'{key}[：:]\s*(.+?)(?=\n|$)'
        match = re.search(pattern, content, re.MULTILINE)
        return match.group(1).strip() if match else default
    
    async def practice_mode(self, question: str, connection_id: int = 0) -> str:
        """
        面談練習モード
        
        Args:
            question: 質問文
            connection_id: 接続ID
        
        Returns:
            AI応答テキスト
        """
        try:
            # AIが応答を生成
            response = await self.interview_service.generate_interview_response(
                question, connection_id, interview_type="general"
            )
            
            # 業界用語の説明を追加
            response = self._enhance_response_with_terms(response, question)
            
            return response
        
        except Exception as e:
            logger.error(f"練習モードエラー: {e}")
            return "申し訳ございません。応答の生成に失敗しました。"
    
    def _enhance_response_with_terms(self, response: str, question: str) -> str:
        """業界用語の説明を追加"""
        enhanced_response = response
        
        for term, definition in self.industry_terms.items():
            if term in question and term not in enhanced_response:
                enhanced_response += f"\n（補足: {term}は{definition}のことです）"
        
        return enhanced_response
    
    def get_practice_questions(self) -> List[str]:
        """練習用の質問リストを取得"""
        return self.question_lists
    
    def get_info_summary(self) -> Dict:
        """設定されている情報のサマリーを取得"""
        return {
            "company_name": self.company_name,
            "has_company_info": bool(self.interview_service.company_info),
            "has_candidate_info": bool(self.interview_service.candidate_info),
            "questions_count": len(self.question_lists),
            "industry_terms_count": len(self.industry_terms),
            "demo_data_available": bool(self.demo_data)
        }
