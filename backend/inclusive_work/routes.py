"""
インクルーシブ雇用AIプラットフォーム - APIルート
"""
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException

from .accessibility import chat as accessibility_chat
from .agents import agent_orchestrator
from .matching import match_jobs
from .models import (AgentTaskRequest, ChatRequest, MatchingRequest,
                     UXEvaluationRequest)
from .ux_evaluation import EVALUATION_ITEMS, evaluate_url

# 認証はオプション（障害者求職者が利用しやすいよう公開APIも検討）
try:
    from auth.jwt_auth import get_current_active_user
    from auth.rbac import require_permission

    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False

router = APIRouter(prefix="/api/v1/inclusive-work", tags=["インクルーシブ雇用AI"])


def _optional_auth():
    """認証をオプションにする（UEP統合時は認証あり）"""
    if AUTH_AVAILABLE:
        return Depends(get_current_active_user)
    return None


@router.get("/status")
async def status():
    """プラットフォーム状態"""
    return {
        "name": "インクルーシブ雇用AIプラットフォーム",
        "version": "1.0.0",
        "features": ["matching", "accessibility_chat", "ux_evaluation", "agents"],
        "description": "障害者雇用マッチング + アクセシビリティ特化AI + 当事者視点UX評価",
    }


@router.post("/matching")
async def matching(request: MatchingRequest):
    """求人マッチング"""
    jobs = match_jobs(request)
    return {"matches": jobs, "count": len(jobs)}


@router.post("/chat")
async def chat_endpoint(request: ChatRequest):
    """アクセシビリティ特化AIチャット"""
    result = await accessibility_chat(
        message=request.message,
        voice_input=request.voice_input or False,
        simple_ui=request.simple_ui or False,
    )
    return result


@router.post("/ux-evaluation")
async def ux_evaluation(request: UXEvaluationRequest):
    """当事者視点UX評価"""
    result = evaluate_url(request)
    return result


@router.get("/ux-evaluation/items")
async def ux_evaluation_items():
    """評価項目一覧"""
    return {"items": EVALUATION_ITEMS}


@router.post("/agent")
async def agent_task(request: AgentTaskRequest):
    """AIエージェントタスク実行"""
    result = await agent_orchestrator.execute(
        task_type=request.task_type,
        query=request.query,
        context=request.context or {},
    )
    return result
