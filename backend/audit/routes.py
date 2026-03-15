"""
監査ログAPI
フロントの重要操作を永続化
"""
from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from auth.jwt_auth import get_current_active_user

router = APIRouter(prefix="/api/v1/audit", tags=["監査ログ"])

# メモリストア（本番ではDB/Elasticsearch等に永続化）
_audit_logs: List[Dict[str, Any]] = []


class AuditEntryCreate(BaseModel):
    action: str
    detail: str | None = None
    path: str | None = None


@router.post("")
async def create_audit_entry(
    entry: AuditEntryCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """監査ログを記録"""
    item = {
        "action": entry.action,
        "detail": entry.detail,
        "path": entry.path,
        "username": current_user.get("username"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _audit_logs.append(item)
    if len(_audit_logs) > 10000:
        _audit_logs.pop(0)
    return {"ok": True}


@router.get("")
async def list_audit_logs(
    limit: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """監査ログ一覧（管理者向け・簡易実装）"""
    if "admin" not in current_user.get("roles", []):
        return {"logs": [], "message": "Admin only"}
    return {"logs": list(reversed(_audit_logs[-limit:]))}
