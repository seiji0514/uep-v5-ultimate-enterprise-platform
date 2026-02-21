"""
統合ビジネスプラットフォーム - Pydanticモデル
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

# ========== 業務効率化・DX ==========


class WorkflowStatus(str, Enum):
    DRAFT = "draft"
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class WorkflowCreate(BaseModel):
    """ワークフロー作成"""

    name: str
    workflow_type: str  # approval, request, notification
    initiator_id: str
    description: Optional[str] = None
    steps: Optional[List[Dict[str, Any]]] = None


class ApprovalRequestCreate(BaseModel):
    """申請・承認リクエスト作成"""

    workflow_id: str
    title: str
    content: str
    amount: Optional[float] = None
    category: Optional[str] = None  # expense, leave, purchase, etc.


class RPAJobCreate(BaseModel):
    """RPAジョブ作成"""

    name: str
    task_type: str  # data_entry, report_generation, notification
    schedule: Optional[str] = None  # cron式
    config: Optional[Dict[str, Any]] = None


# ========== 人材・組織 ==========


class DisabilitySupportCreate(BaseModel):
    """障害者雇用支援 - 配慮登録"""

    employee_id: str
    disability_type: str  # physical, visual, hearing, etc.
    disability_grade: Optional[str] = None
    accommodations: List[str]  # 必要な配慮事項
    remote_work_eligible: bool = True
    notes: Optional[str] = None


class OnboardingTaskCreate(BaseModel):
    """オンボーディングタスク作成"""

    employee_id: str
    task_name: str
    category: str  # document, training, equipment, access
    due_date: Optional[str] = None
    assignee_id: Optional[str] = None


class OnboardingFromTemplateRequest(BaseModel):
    """テンプレートからオンボーディング作成"""

    employee_id: str
    template: str = "standard"


class SkillMatchingRequest(BaseModel):
    """スキルマッチングリクエスト"""

    project_id: str
    required_skills: List[str]
    preferred_skills: Optional[List[str]] = None
    experience_level: Optional[str] = None  # junior, mid, senior


class RegisterSkillsRequest(BaseModel):
    """社員スキル登録リクエスト"""

    employee_id: str
    skills: List[str]
    experience_level: str = "mid"


# ========== 顧客対応・CX ==========


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    RESOLVED = "resolved"
    CLOSED = "closed"


class TicketCreate(BaseModel):
    """チケット作成"""

    customer_id: str
    subject: str
    description: str
    priority: TicketPriority = TicketPriority.MEDIUM
    category: Optional[str] = None


class ChatMessageCreate(BaseModel):
    """チャットメッセージ作成"""

    ticket_id: Optional[str] = None
    customer_id: Optional[str] = None
    message: str
    use_ai_response: bool = True  # AIチャットボットで応答するか


class TicketStatusUpdate(BaseModel):
    """チケットステータス更新"""

    status: str
    assigned_to: Optional[str] = None
