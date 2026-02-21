"""
統合ビジネスプラットフォーム - 監査ログ
実用的最高難易度: セキュリティ・コンプライアンス統合
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class AuditAction(str, Enum):
    WORKFLOW_CREATE = "workflow.create"
    WORKFLOW_UPDATE = "workflow.update"
    APPROVAL_CREATE = "approval.create"
    APPROVAL_APPROVE = "approval.approve"
    APPROVAL_REJECT = "approval.reject"
    RPA_JOB_CREATE = "rpa.create"
    RPA_JOB_RUN = "rpa.run"
    DISABILITY_SUPPORT_REGISTER = "hr.disability_support.register"
    ONBOARDING_TASK_CREATE = "hr.onboarding.create"
    ONBOARDING_TASK_COMPLETE = "hr.onboarding.complete"
    SKILL_MATCHING = "hr.skill_matching"
    TICKET_CREATE = "customer.ticket.create"
    TICKET_UPDATE = "customer.ticket.update"
    CHATBOT_QUERY = "customer.chatbot.query"


class AuditLogger:
    """監査ログ記録"""

    def __init__(self, max_entries: int = 10000):
        self._logs: List[Dict[str, Any]] = []
        self._max_entries = max_entries

    def log(
        self,
        action: AuditAction,
        user_id: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
    ) -> Dict[str, Any]:
        """監査ログを記録"""
        entry = {
            "id": f"audit_{len(self._logs)}_{datetime.utcnow().timestamp()}",
            "action": action.value,
            "user_id": user_id,
            "resource_type": resource_type,
            "resource_id": resource_id,
            "details": details or {},
            "ip_address": ip_address,
            "timestamp": datetime.utcnow().isoformat(),
        }
        self._logs.append(entry)
        if len(self._logs) > self._max_entries:
            self._logs = self._logs[-self._max_entries:]
        return entry

    def get_logs(
        self,
        action: Optional[AuditAction] = None,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """監査ログを取得"""
        logs = self._logs
        if action:
            logs = [l for l in logs if l["action"] == action.value]
        if user_id:
            logs = [l for l in logs if l["user_id"] == user_id]
        if resource_type:
            logs = [l for l in logs if l["resource_type"] == resource_type]
        return list(reversed(logs[-limit:]))


audit_logger = AuditLogger()
