"""
インクルーシブ雇用AI - データモデル
"""
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class DisabilityType(str, Enum):
    """障害種別"""

    PHYSICAL = "physical"  # 身体
    INTELLECTUAL = "intellectual"  # 知的
    MENTAL = "mental"  # 精神
    OTHER = "other"


class WorkStyle(str, Enum):
    """勤務形態"""

    REMOTE = "remote"
    ONSITE = "onsite"
    HYBRID = "hybrid"


class MatchingRequest(BaseModel):
    """マッチングリクエスト"""

    skills: List[str] = []
    disability_type: Optional[DisabilityType] = None
    work_style: Optional[WorkStyle] = None
    location: Optional[str] = None
    keywords: Optional[List[str]] = None


class ChatRequest(BaseModel):
    """アクセシビリティAIチャットリクエスト"""

    message: str
    voice_input: Optional[bool] = False  # 音声入力フラグ
    simple_ui: Optional[bool] = False  # 簡易UIモード


class UXEvaluationRequest(BaseModel):
    """UX評価リクエスト"""

    url: str
    check_items: Optional[List[str]] = None  # 評価項目（省略時は全項目）


class AgentTaskRequest(BaseModel):
    """エージェントタスクリクエスト"""

    task_type: str  # matching, consultation, evaluation
    query: str
    context: Optional[Dict[str, Any]] = None
