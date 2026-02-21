"""
統合ビジネスプラットフォーム APIエンドポイント
業務効率化・DX / 人材・組織 / 顧客対応・CX の3システム統合
実用的最高難易度: メトリクス・監査・イベント統合
"""
import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from . import events, metrics
from .audit import AuditAction, audit_logger
from .customer_support import chatbot_manager, ticket_manager
from .hr import (disability_support_manager, onboarding_manager,
                 skill_matching_manager)
from .models import (ApprovalRequestCreate, ChatMessageCreate,
                     DisabilitySupportCreate, OnboardingFromTemplateRequest,
                     OnboardingTaskCreate, RegisterSkillsRequest, RPAJobCreate,
                     SkillMatchingRequest, TicketCreate, TicketStatusUpdate,
                     WorkflowCreate)
from .workflow import rpa_manager, workflow_manager

router = APIRouter(prefix="/api/v1/unified-business", tags=["統合ビジネスプラットフォーム"])


def _user_id(user: Dict[str, Any]) -> str:
    return user.get("username") or user.get("sub") or "unknown"


# ========== サマリー・ヘルスチェック ==========


@router.get("/audit-logs", response_model=List[Dict[str, Any]])
@require_permission("read")
async def get_audit_logs(
    action: Optional[str] = None,
    user_id: Optional[str] = None,
    resource_type: Optional[str] = None,
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """監査ログ取得（セキュリティ・コンプライアンス）"""
    audit_action = None
    if action:
        try:
            audit_action = AuditAction(action)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Invalid action: {action}")
    return audit_logger.get_logs(
        action=audit_action,
        user_id=user_id,
        resource_type=resource_type,
        limit=limit,
    )


@router.get("/summary")
@require_permission("read")
async def get_platform_summary(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """統合プラットフォームのサマリー"""
    return {
        "platform": "統合ビジネスプラットフォーム",
        "version": "1.0.0",
        "modules": {
            "業務効率化・DX": {
                "workflows": len(workflow_manager.list_workflows()),
                "approval_requests": len(workflow_manager.list_approval_requests()),
                "rpa_jobs": len(rpa_manager.list_jobs()),
            },
            "人材・組織": {
                "disability_supports": len(disability_support_manager.list_supports()),
                "onboarding_tasks": len(onboarding_manager.list_tasks()),
            },
            "顧客対応・CX": {
                "tickets": len(ticket_manager.list_tickets()),
            },
        },
    }


# ========== 業務効率化・DX ==========


@router.get("/workflows", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_workflows(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ワークフロー一覧"""
    return workflow_manager.list_workflows()


@router.post("/workflows", status_code=status.HTTP_201_CREATED)
@require_permission("write")
async def create_workflow(
    data: WorkflowCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ワークフローを作成"""
    w = workflow_manager.create_workflow(
        name=data.name,
        workflow_type=data.workflow_type,
        initiator_id=data.initiator_id,
        description=data.description,
        steps=data.steps,
    )
    metrics.workflow_created_total.labels(workflow_type=data.workflow_type).inc()
    audit_logger.log(
        AuditAction.WORKFLOW_CREATE,
        _user_id(current_user),
        "workflow",
        w["id"],
        {"name": data.name},
    )
    events.publish_workflow_event("workflow.created", w["id"], {"name": data.name})
    return w


@router.get("/approval-requests", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_approval_requests(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """申請・承認リクエスト一覧"""
    return workflow_manager.list_approval_requests()


@router.post("/approval-requests", status_code=status.HTTP_201_CREATED)
@require_permission("write")
async def create_approval_request(
    data: ApprovalRequestCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """申請・承認リクエストを作成（条件分岐で多段階承認ルート自動決定）"""
    r = workflow_manager.create_approval_request(
        workflow_id=data.workflow_id,
        title=data.title,
        content=data.content,
        amount=data.amount,
        category=data.category,
    )
    metrics.approval_requests_total.labels(status="pending").inc()
    audit_logger.log(
        AuditAction.APPROVAL_CREATE,
        _user_id(current_user),
        "approval_request",
        r["id"],
        {"title": data.title},
    )
    events.publish_approval_event("approval.created", r["id"], {"title": data.title})
    return r


@router.post("/approval-requests/{request_id}/approve")
@require_permission("write")
async def approve_request(
    request_id: str,
    approved: bool,
    comment: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """申請を承認/却下（多段階承認対応）"""
    result = workflow_manager.approve_request(
        request_id=request_id,
        approver_id=_user_id(current_user),
        approved=approved,
        comment=comment,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Request not found")
    metrics.approval_requests_total.labels(status=result["status"]).inc()
    act = AuditAction.APPROVAL_APPROVE if approved else AuditAction.APPROVAL_REJECT
    audit_logger.log(
        act,
        _user_id(current_user),
        "approval_request",
        request_id,
        {"approved": approved},
    )
    events.publish_approval_event(
        "approval.approved" if approved else "approval.rejected",
        request_id,
        {"approved": approved},
    )
    return result


@router.get("/rpa/jobs", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_rpa_jobs(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """RPAジョブ一覧"""
    return rpa_manager.list_jobs()


@router.post("/rpa/jobs", status_code=status.HTTP_201_CREATED)
@require_permission("write")
async def create_rpa_job(
    data: RPAJobCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """RPAジョブを作成"""
    j = rpa_manager.create_job(
        name=data.name,
        task_type=data.task_type,
        schedule=data.schedule,
        config=data.config,
    )
    audit_logger.log(
        AuditAction.RPA_JOB_CREATE,
        _user_id(current_user),
        "rpa_job",
        j["id"],
        {"name": data.name},
    )
    return j


@router.post("/rpa/jobs/{job_id}/run")
@require_permission("write")
async def run_rpa_job(
    job_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """RPAジョブを実行"""
    t0 = time.perf_counter()
    result = rpa_manager.run_job(job_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Job not found")
    dur = time.perf_counter() - t0
    metrics.rpa_jobs_executed_total.labels(
        task_type=result.get("task_type", "unknown"), status=result["status"]
    ).inc()
    metrics.rpa_job_duration_seconds.labels(
        task_type=result.get("task_type", "unknown")
    ).observe(dur)
    audit_logger.log(
        AuditAction.RPA_JOB_RUN,
        _user_id(current_user),
        "rpa_job",
        job_id,
        {"status": result["status"]},
    )
    return result


# ========== 人材・組織 ==========


@router.get("/hr/disability-supports", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_disability_supports(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """障害者雇用支援 - 配慮登録一覧"""
    return disability_support_manager.list_supports()


@router.get("/hr/disability-supports/checklist")
@require_permission("read")
async def get_accommodation_checklist(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """合理的配慮チェックリスト"""
    return disability_support_manager.get_accommodation_checklist()


@router.post("/hr/disability-supports", status_code=status.HTTP_201_CREATED)
@require_permission("write")
async def register_disability_support(
    data: DisabilitySupportCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """障害者雇用支援 - 配慮を登録"""
    s = disability_support_manager.register_support(
        employee_id=data.employee_id,
        disability_type=data.disability_type,
        accommodations=data.accommodations,
        disability_grade=data.disability_grade,
        remote_work_eligible=data.remote_work_eligible,
        notes=data.notes,
    )
    metrics.disability_supports_total.inc()
    audit_logger.log(
        AuditAction.DISABILITY_SUPPORT_REGISTER,
        _user_id(current_user),
        "disability_support",
        s.get("id", data.employee_id),
        {"employee_id": data.employee_id},
    )
    return s


@router.get("/hr/onboarding/tasks", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_onboarding_tasks(
    employee_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """オンボーディングタスク一覧"""
    return onboarding_manager.list_tasks(employee_id=employee_id)


@router.post("/hr/onboarding/tasks", status_code=status.HTTP_201_CREATED)
@require_permission("write")
async def create_onboarding_task(
    data: OnboardingTaskCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """オンボーディングタスクを作成"""
    t = onboarding_manager.create_task(
        employee_id=data.employee_id,
        task_name=data.task_name,
        category=data.category,
        due_date=data.due_date,
        assignee_id=data.assignee_id,
    )
    metrics.onboarding_tasks_total.labels(status="pending").inc()
    audit_logger.log(
        AuditAction.ONBOARDING_TASK_CREATE,
        _user_id(current_user),
        "onboarding_task",
        t["id"],
        {"task_name": data.task_name},
    )
    return t


@router.post("/hr/onboarding/tasks/from-template")
@require_permission("write")
async def create_onboarding_from_template(
    data: OnboardingFromTemplateRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """テンプレートからオンボーディングタスクを一括作成"""
    return onboarding_manager.create_from_template(
        employee_id=data.employee_id,
        template=data.template,
    )


@router.post("/hr/onboarding/tasks/{task_id}/complete")
@require_permission("write")
async def complete_onboarding_task(
    task_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """オンボーディングタスクを完了"""
    result = onboarding_manager.complete_task(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Task not found")
    metrics.onboarding_tasks_total.labels(status="completed").inc()
    audit_logger.log(
        AuditAction.ONBOARDING_TASK_COMPLETE,
        _user_id(current_user),
        "onboarding_task",
        task_id,
        {},
    )
    return result


@router.post("/hr/skill-matching/register")
@require_permission("write")
async def register_employee_skills(
    data: RegisterSkillsRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """社員スキルを登録"""
    return skill_matching_manager.register_employee_skills(
        employee_id=data.employee_id,
        skills=data.skills,
        experience_level=data.experience_level,
    )


@router.post("/hr/skill-matching/find")
@require_permission("read")
async def find_skill_matches(
    data: SkillMatchingRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """スキルマッチング"""
    r = skill_matching_manager.find_matches(
        required_skills=data.required_skills,
        preferred_skills=data.preferred_skills,
        experience_level=data.experience_level,
    )
    metrics.skill_matches_total.inc()
    audit_logger.log(
        AuditAction.SKILL_MATCHING,
        _user_id(current_user),
        "skill_matching",
        "query",
        {"required_skills": data.required_skills},
    )
    return r


# ========== 顧客対応・CX ==========


@router.get("/customer/tickets", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_tickets(
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """チケット一覧"""
    return ticket_manager.list_tickets(
        status=status,
        customer_id=customer_id,
    )


@router.post("/customer/tickets", status_code=status.HTTP_201_CREATED)
@require_permission("write")
async def create_ticket(
    data: TicketCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """チケットを作成"""
    t = ticket_manager.create_ticket(
        customer_id=data.customer_id,
        subject=data.subject,
        description=data.description,
        priority=data.priority.value,
        category=data.category,
    )
    metrics.tickets_total.labels(priority=data.priority.value, status="open").inc()
    audit_logger.log(
        AuditAction.TICKET_CREATE,
        _user_id(current_user),
        "ticket",
        t["id"],
        {"subject": data.subject},
    )
    events.publish_ticket_event("ticket.created", t["id"], {"subject": data.subject})
    return t


@router.patch("/customer/tickets/{ticket_id}")
@require_permission("write")
async def update_ticket_status(
    ticket_id: str,
    data: TicketStatusUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """チケットステータスを更新"""
    result = ticket_manager.update_ticket_status(
        ticket_id=ticket_id,
        status=data.status,
        assigned_to=data.assigned_to,
    )
    if result is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    audit_logger.log(
        AuditAction.TICKET_UPDATE,
        _user_id(current_user),
        "ticket",
        ticket_id,
        {"status": data.status},
    )
    events.publish_ticket_event("ticket.updated", ticket_id, {"status": data.status})
    return result


@router.post("/customer/chat")
async def chat(
    data: ChatMessageCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """AIチャットボット（認証不要で公開可能にする場合は別途実装）"""
    r = chatbot_manager.chat(
        message=data.message,
        ticket_id=data.ticket_id,
        customer_id=data.customer_id,
    )
    metrics.chatbot_requests_total.inc()
    audit_logger.log(
        AuditAction.CHATBOT_QUERY,
        _user_id(current_user),
        "chatbot",
        data.ticket_id or "standalone",
        {"ticket_id": data.ticket_id},
    )
    return r
