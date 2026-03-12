"""
レガシー移行ツール API
メインフレーム・オンプレからクラウドERPへの移行支援
"""
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .migration import legacy_migration_manager
from .models import MigrationJobCreate, MigrationValidationRequest

router = APIRouter(prefix="/api/v1/legacy-migration", tags=["レガシー移行ツール"])


@router.get("/summary")
@require_permission("read")
async def get_migration_summary(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """移行ツールサマリー"""
    return legacy_migration_manager.get_summary()


@router.post("/jobs", response_model=Dict[str, Any])
@require_permission("write")
async def create_migration_job(
    body: MigrationJobCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """移行ジョブ作成"""
    return legacy_migration_manager.create_job(
        source_type=body.source_type,
        source_config=body.source_config,
        target_system=body.target_system,
        mapping=body.mapping,
    )


@router.get("/jobs", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_migration_jobs(
    limit: int = 50,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """移行ジョブ一覧"""
    return legacy_migration_manager.list_jobs(limit=limit)


@router.get("/jobs/{job_id}")
@require_permission("read")
async def get_migration_job(
    job_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """移行ジョブ詳細"""
    job = legacy_migration_manager.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@router.post("/jobs/{job_id}/run")
@require_permission("write")
async def run_migration(
    job_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """移行実行"""
    return legacy_migration_manager.run_migration(job_id)


@router.post("/validate")
@require_permission("write")
async def validate_migration(
    body: MigrationValidationRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """移行検証（移行前後のデータ比較）"""
    return legacy_migration_manager.validate_migration(body.job_id, body.compare_field)
