"""
面談特化の応答生成サービス
"""
import logging
from typing import Dict, Optional, List
from collections import defaultdict

logger = logging.getLogger(__name__)

# OpenAI APIの使用可否
USE_OPENAI_API = False
try:
    from openai import OpenAI
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        USE_OPENAI_API = True
        openai_client = OpenAI(api_key=api_key)
except:
    pass


class InterviewResponseService:
    """
    面談特化の応答生成サービス
    
    機能:
    - 面談用の最適化された応答生成
    - よくある質問への即答
    - 会話の文脈理解
    - 先方情報と自分の情報を活用した応答生成
    """
    
    def __init__(
        self,
        candidate_info: Optional[Dict] = None,
        company_info: Optional[Dict] = None,
        interviewer_info: Optional[Dict] = None
    ):
        """
        初期化
        
        Args:
            candidate_info: 応募者（自分）の情報
                - name: 名前
                - experience: 職務経歴
                - skills: スキルリスト
                - motivation: 志望動機
                - strengths: 強み
                - weaknesses: 弱み
            company_info: 企業（先方）の情報
                - name: 企業名
                - industry: 業界
                - business: 事業内容
                - values: 企業理念・価値観
                - culture: 企業文化
                - benefits: 福利厚生
            interviewer_info: 面接官の情報
                - name: 名前
                - position: 役職
                - department: 部署
                - background: 経歴・背景
        """
        self.candidate_info = candidate_info or {}
        self.company_info = company_info or {}
        self.interviewer_info = interviewer_info or {}
        self.conversation_history: Dict[int, List[Dict[str, str]]] = defaultdict(list)
        
        # よくある質問と回答のテンプレート
        self.common_qa = {
            "自己紹介": self._generate_introduction(),
            "志望動機": self._generate_motivation(),
            "強み": self._generate_strengths(),
            "弱み": self._generate_weaknesses(),
            "転職理由": self._generate_reason_for_change(),
        }
    
    def _generate_introduction(self) -> str:
        """自己紹介のテンプレート"""
        if self.candidate_info.get("name"):
            return f"こんにちは、{self.candidate_info['name']}と申します。"
        return "こんにちは、よろしくお願いします。"
    
    def _generate_motivation(self) -> str:
        """志望動機のテンプレート"""
        motivation = self.candidate_info.get("motivation", "")
        if motivation:
            return motivation
        return "貴社の[具体的な理由]に共感し、[自分のスキル]を活かして貢献したいと考えています。"
    
    def _generate_strengths(self) -> str:
        """強みのテンプレート"""
        skills = self.candidate_info.get("skills", [])
        if skills:
            return f"私の強みは{', '.join(skills[:3])}です。具体的には[具体例]があります。"
        return "私の強みは[スキル]です。"
    
    def _generate_weaknesses(self) -> str:
        """弱みのテンプレート"""
        return "改善の余地がある点として[弱み]がありますが、[改善策]を実践しています。"
    
    def _generate_reason_for_change(self) -> str:
        """転職理由のテンプレート"""
        return "[前職での経験]を活かし、[新しい環境での目標]を実現したいと考えています。"
    
    def _detect_question_type(self, text: str) -> Optional[str]:
        """質問のタイプを検出"""
        text_lower = text.lower()
        
        if any(keyword in text_lower for keyword in ["自己紹介", "名前", "どなた"]):
            return "自己紹介"
        elif any(keyword in text_lower for keyword in ["志望動機", "なぜ", "理由"]):
            return "志望動機"
        elif any(keyword in text_lower for keyword in ["強み", "得意", "長所"]):
            return "強み"
        elif any(keyword in text_lower for keyword in ["弱み", "苦手", "短所"]):
            return "弱み"
        elif any(keyword in text_lower for keyword in ["転職", "退職", "理由"]):
            return "転職理由"
        
        return None
    
    async def generate_interview_response(
        self,
        question: str,
        connection_id: int,
        interview_type: str = "general"
    ) -> str:
        """
        面談用の応答を生成
        
        Args:
            question: 質問文
            connection_id: 接続ID
            interview_type: 面談タイプ（general, technical, cultural）
        
        Returns:
            AI応答テキスト
        """
        try:
            # よくある質問かチェック
            question_type = self._detect_question_type(question)
            if question_type and question_type in self.common_qa:
                response = self.common_qa[question_type]
                logger.info(f"よくある質問に即答: {question_type}")
            else:
                # AIで応答生成
                response = await self._generate_ai_response(
                    question, connection_id, interview_type
                )
            
            # 会話履歴に追加
            self.conversation_history[connection_id].append({
                "role": "user",
                "content": question
            })
            self.conversation_history[connection_id].append({
                "role": "assistant",
                "content": response
            })
            
            return response
        
        except Exception as e:
            logger.error(f"応答生成エラー: {e}")
            return "申し訳ございません。もう一度お聞かせいただけますか？"
    
    async def _generate_ai_response(
        self,
        question: str,
        connection_id: int,
        interview_type: str
    ) -> str:
        """AIで応答を生成"""
        
        # 面談タイプに応じたシステムプロンプト
        system_prompts = {
            "general": """
あなたは面接での応答をサポートするAIアシスタントです。
自然で誠実な応答を生成してください。
簡潔で明確、具体的な事例を含む応答を心がけてください。
先方の企業情報や面接官の情報を考慮し、適切な応答を生成してください。
""",
            "technical": """
あなたは技術面接での応答をサポートするAIアシスタントです。
技術的な質問に対して、具体的で正確な回答を生成してください。
コード例や実装例を含めることができます。
企業の技術スタックや事業内容を考慮した応答を心がけてください。
""",
            "cultural": """
あなたは文化適合性面接での応答をサポートするAIアシスタントです。
チームワーク、価値観、働き方について自然に応答してください。
企業の文化や価値観に共感を示しつつ、自分の価値観も伝える応答を生成してください。
"""
        }
        
        system_prompt = system_prompts.get(interview_type, system_prompts["general"])
        
        # 応募者（自分）の情報を追加
        if self.candidate_info:
            candidate_context = f"""
【応募者（自分）の情報】
- 名前: {self.candidate_info.get('name', 'N/A')}
- 職務経歴: {self.candidate_info.get('experience', 'N/A')}
- スキル: {', '.join(self.candidate_info.get('skills', [])) if isinstance(self.candidate_info.get('skills'), list) else self.candidate_info.get('skills', 'N/A')}
- 志望動機: {self.candidate_info.get('motivation', 'N/A')}
- 強み: {self.candidate_info.get('strengths', 'N/A')}
- 弱み: {self.candidate_info.get('weaknesses', 'N/A')}
"""
            system_prompt += candidate_context
        
        # 企業（先方）の情報を追加
        if self.company_info:
            company_context = f"""
【企業（先方）の情報】
- 企業名: {self.company_info.get('name', 'N/A')}
- 業界: {self.company_info.get('industry', 'N/A')}
- 事業内容: {self.company_info.get('business', 'N/A')}
- 企業理念・価値観: {self.company_info.get('values', 'N/A')}
- 企業文化: {self.company_info.get('culture', 'N/A')}
- 福利厚生: {self.company_info.get('benefits', 'N/A')}
"""
            system_prompt += company_context
        
        # 面接官の情報を追加
        if self.interviewer_info:
            interviewer_context = f"""
【面接官の情報】
- 名前: {self.interviewer_info.get('name', 'N/A')}
- 役職: {self.interviewer_info.get('position', 'N/A')}
- 部署: {self.interviewer_info.get('department', 'N/A')}
- 経歴・背景: {self.interviewer_info.get('background', 'N/A')}
"""
            system_prompt += interviewer_context
        
        # 応答のガイドラインを追加
        if self.company_info or self.interviewer_info:
            system_prompt += """
【応答のガイドライン】
- 先方の企業情報や価値観を理解した上で応答してください
- 自分の経験やスキルを先方のニーズに結びつけて説明してください
- 企業の文化や理念に共感を示しつつ、自分の価値観も伝えてください
- 面接官の背景を考慮し、適切なレベルで応答してください
"""
        
        # 会話履歴を取得
        history = self.conversation_history[connection_id][-10:]
        
        # メッセージを構築
        messages = [{"role": "system", "content": system_prompt}]
        
        for msg in history:
            if msg["role"] in ["user", "assistant"]:
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        messages.append({"role": "user", "content": question})
        
        # OpenAI APIを使用
        if USE_OPENAI_API:
            try:
                response = openai_client.chat.completions.create(
                    model="gpt-4",  # より高品質な応答のためにGPT-4を使用
                    messages=messages,
                    max_tokens=300,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"OpenAI APIエラー: {e}")
        
        # フォールバック: 簡易応答
        return self._generate_fallback_response(question)
    
    def _generate_fallback_response(self, question: str) -> str:
        """フォールバック応答"""
        return f"「{question}」についてですね。{self.candidate_info.get('experience', '私の経験')}を踏まえてお答えします。"
    
    def set_candidate_info(self, candidate_info: Dict):
        """応募者（自分）の情報を設定"""
        self.candidate_info = candidate_info
        # よくある質問のテンプレートを更新
        self.common_qa = {
            "自己紹介": self._generate_introduction(),
            "志望動機": self._generate_motivation(),
            "強み": self._generate_strengths(),
            "弱み": self._generate_weaknesses(),
            "転職理由": self._generate_reason_for_change(),
        }
        logger.info("応募者情報を更新しました")
    
    def set_company_info(self, company_info: Dict):
        """企業（先方）の情報を設定"""
        self.company_info = company_info
        logger.info(f"企業情報を更新しました: {company_info.get('name', 'N/A')}")
    
    def set_interviewer_info(self, interviewer_info: Dict):
        """面接官の情報を設定"""
        self.interviewer_info = interviewer_info
        logger.info(f"面接官情報を更新しました: {interviewer_info.get('name', 'N/A')}")
    
    def set_all_info(
        self,
        candidate_info: Optional[Dict] = None,
        company_info: Optional[Dict] = None,
        interviewer_info: Optional[Dict] = None
    ):
        """すべての情報を一度に設定"""
        if candidate_info:
            self.set_candidate_info(candidate_info)
        if company_info:
            self.set_company_info(company_info)
        if interviewer_info:
            self.set_interviewer_info(interviewer_info)
    
    def get_info_summary(self) -> Dict:
        """設定されている情報のサマリーを取得"""
        return {
            "candidate": {
                "has_info": bool(self.candidate_info),
                "name": self.candidate_info.get("name", "未設定"),
                "skills_count": len(self.candidate_info.get("skills", [])) if isinstance(self.candidate_info.get("skills"), list) else 0
            },
            "company": {
                "has_info": bool(self.company_info),
                "name": self.company_info.get("name", "未設定"),
                "industry": self.company_info.get("industry", "未設定")
            },
            "interviewer": {
                "has_info": bool(self.interviewer_info),
                "name": self.interviewer_info.get("name", "未設定"),
                "position": self.interviewer_info.get("position", "未設定")
            }
        }
    
    def reset_conversation(self, connection_id: int):
        """会話履歴をリセット"""
        if connection_id in self.conversation_history:
            del self.conversation_history[connection_id]
