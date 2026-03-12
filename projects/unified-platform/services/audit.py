"""Phase 2: Audit Log - Compliance"""
from typing import Optional, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert

from models import AuditLog
from config import get_config


async def write_audit(
    db: AsyncSession,
    action: str,
    resource: str,
    resource_id: Optional[str] = None,
    user_id: Optional[str] = None,
    details: Optional[dict] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> None:
    """Phase 2: Write audit log - who, when, what"""
    if not get_config()["audit_log_enabled"]:
        return
    stmt = insert(AuditLog).values(
        action=action,
        resource=resource,
        resource_id=resource_id,
        user_id=user_id,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent,
    )
    await db.execute(stmt)
