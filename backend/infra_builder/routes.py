"""
インフラ構築専用システム - APIエンドポイント

インフラ構築に特化したワークフロー管理API。
設計 → 構築 → デプロイ → 検証の一連の流れを管理。
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .models import (
    BlueprintCreate,
    BuildProjectCreate,
    BuildProjectStatus,
    PipelineCreate,
    PipelineStatus,
)
from .services import InfraBuilderService

router = APIRouter(prefix="/api/v1/infra-builder", tags=["インフラ構築専用"])

# シングルトンサービス
infra_builder_service = InfraBuilderService()


@router.get("/dashboard")
@require_permission("read")
async def get_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ダッシュボードサマリー取得"""
    return infra_builder_service.get_dashboard()


@router.get("/projects", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_projects(
    status_filter: Optional[str] = None,
    provider: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """構築プロジェクト一覧"""
    status_enum = BuildProjectStatus(status_filter) if status_filter else None
    return infra_builder_service.list_projects(status=status_enum, provider=provider)


@router.post(
    "/projects",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
@require_permission("manage_infrastructure")
async def create_project(
    project_data: BuildProjectCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """構築プロジェクト作成"""
    return infra_builder_service.create_project(
        name=project_data.name,
        description=project_data.description,
        target_provider=project_data.target_provider,
        blueprint=project_data.blueprint,
        created_by=current_user.get("username"),
    )


@router.get("/projects/{project_id}", response_model=Dict[str, Any])
@require_permission("read")
async def get_project(
    project_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """構築プロジェクト取得"""
    project = infra_builder_service.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project not found: {project_id}",
        )
    return project


@router.get("/blueprints", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_blueprints(
    provider: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ブループリント一覧"""
    return infra_builder_service.list_blueprints(provider=provider)


@router.post(
    "/blueprints",
    response_model=Dict[str, Any],
    status_code=status.HTTP_201_CREATED,
)
@require_permission("manage_infrastructure")
async def create_blueprint(
    blueprint_data: BlueprintCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ブループリント作成"""
    return infra_builder_service.create_blueprint(
        name=blueprint_data.name,
        provider=blueprint_data.provider,
        content=blueprint_data.content,
        variables=blueprint_data.variables,
        description=blueprint_data.description,
        created_by=current_user.get("username"),
    )


@router.get("/pipelines", response_model=List[Dict[str, Any]])
@require_permission("read")
async def list_pipelines(
    project_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """パイプライン実行一覧"""
    status_enum = PipelineStatus(status_filter) if status_filter else None
    return infra_builder_service.list_pipelines(
        project_id=project_id,
        status=status_enum,
    )


@router.post("/pipelines/run", response_model=Dict[str, Any])
@require_permission("manage_infrastructure")
async def run_pipeline(
    pipeline_data: PipelineCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """パイプライン実行"""
    try:
        return infra_builder_service.run_pipeline(
            project_id=pipeline_data.project_id,
            stages=pipeline_data.stages,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
