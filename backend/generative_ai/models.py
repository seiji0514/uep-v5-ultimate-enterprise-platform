"""
生成AI関連のデータモデル
"""
from typing import Any, Dict, Optional

from pydantic import BaseModel


class GenerateRequest(BaseModel):
    """テキスト生成リクエスト"""

    prompt: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7


class RAGRequest(BaseModel):
    """RAGリクエスト"""

    query: str
    collection: Optional[str] = None
    context: Optional[str] = None


class ReasoningRequest(BaseModel):
    """推論リクエスト"""

    problem: Optional[str] = None  # 後方互換
    question: Optional[str] = None  # フロントエンド互換
    reasoning_type: str = "cot"
    max_steps: Optional[int] = 5

    def get_problem(self) -> str:
        """問題文を取得（problem または question）"""
        return (self.problem or self.question or "").strip()
