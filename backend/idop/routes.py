"""
IDOP APIエンドポイント
"""
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional, Dict, Any
from datetime import datetime
from .cicd import cicd_pipeline, CICDPipelineModel, PipelineStage, CICDStatus
from .devops import devops_manager, Application, Environment
from .models import (
    CICDPipelineCreate, CICDTrigger, ApplicationCreate, ApplicationDeploy
)
from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

router = APIRouter(prefix="/api/v1/idop", tags=["IDOP"])


@router.get("/pipelines", response_model=List[CICDPipelineModel])
@require_permission("read")
async def list_cicd_pipelines(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """CI/CDパイプライン一覧を取得"""
    pipelines = cicd_pipeline.list_pipelines()
    return pipelines


@router.post("/pipelines", response_model=CICDPipelineModel, status_code=status.HTTP_201_CREATED)
@require_permission("manage_infrastructure")
async def create_cicd_pipeline(
    pipeline_data: CICDPipelineCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """CI/CDパイプラインを作成"""
    stages = [PipelineStage(s) for s in pipeline_data.stages] if pipeline_data.stages else None
    pipeline = cicd_pipeline.create_pipeline(
        name=pipeline_data.name,
        repository=pipeline_data.repository,
        branch=pipeline_data.branch,
        stages=stages,
        created_by=current_user["username"],
        config=pipeline_data.config
    )
    return pipeline


@router.post("/pipelines/{pipeline_id}/trigger")
@require_permission("manage_infrastructure")
async def trigger_pipeline(
    pipeline_id: str,
    trigger_data: CICDTrigger,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """CI/CDパイプラインをトリガー"""
    try:
        run = cicd_pipeline.trigger_pipeline(
            pipeline_id=pipeline_id,
            commit_hash=trigger_data.commit_hash
        )
        return run
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/applications", response_model=List[Application])
@require_permission("read")
async def list_applications(
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """アプリケーション一覧を取得"""
    applications = devops_manager.list_applications()
    return applications


@router.post("/applications", response_model=Application, status_code=status.HTTP_201_CREATED)
@require_permission("manage_infrastructure")
async def register_application(
    app_data: ApplicationCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """アプリケーションを登録"""
    environments = [Environment(e) for e in app_data.environments] if app_data.environments else None
    application = devops_manager.register_application(
        name=app_data.name,
        repository=app_data.repository,
        created_by=current_user["username"],
        description=app_data.description,
        environments=environments
    )
    return application


@router.post("/applications/{application_id}/deploy")
@require_permission("manage_infrastructure")
async def deploy_application(
    application_id: str,
    deploy_data: ApplicationDeploy,
    current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """アプリケーションをデプロイ"""
    try:
        environment = Environment(deploy_data.environment)
        deployment = devops_manager.deploy_application(
            application_id=application_id,
            environment=environment,
            version=deploy_data.version,
            config=deploy_data.config
        )
        return deployment
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
