"""
インフラ構築専用システム - ビジネスロジック
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from .models import (
    BuildProjectStatus,
    BuildStage,
    PipelineStatus,
)


class BuildProject:
    """構築プロジェクト"""

    def __init__(
        self,
        id: str,
        name: str,
        description: Optional[str] = None,
        target_provider: str = "docker",
        blueprint: Optional[Dict[str, Any]] = None,
        status: BuildProjectStatus = BuildProjectStatus.DRAFT,
        current_stage: BuildStage = BuildStage.DESIGN,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        created_by: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.description = description or ""
        self.target_provider = target_provider
        self.blueprint = blueprint or {}
        self.status = status
        self.current_stage = current_stage
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.created_by = created_by or "system"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "target_provider": self.target_provider,
            "blueprint": self.blueprint,
            "status": self.status.value,
            "current_stage": self.current_stage.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by,
        }


class PipelineRun:
    """パイプライン実行"""

    def __init__(
        self,
        id: str,
        project_id: str,
        stages: List[str],
        status: PipelineStatus = PipelineStatus.PENDING,
        current_stage: Optional[str] = None,
        started_at: Optional[datetime] = None,
        completed_at: Optional[datetime] = None,
        logs: Optional[List[str]] = None,
    ):
        self.id = id
        self.project_id = project_id
        self.stages = stages
        self.status = status
        self.current_stage = current_stage
        self.started_at = started_at or datetime.utcnow()
        self.completed_at = completed_at
        self.logs = logs or []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "stages": self.stages,
            "status": self.status.value,
            "current_stage": self.current_stage,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "logs": self.logs,
        }


class Blueprint:
    """インフラブループリント"""

    def __init__(
        self,
        id: str,
        name: str,
        provider: str,
        content: str,
        variables: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime] = None,
        created_by: Optional[str] = None,
    ):
        self.id = id
        self.name = name
        self.provider = provider
        self.content = content
        self.variables = variables or {}
        self.description = description or ""
        self.created_at = created_at or datetime.utcnow()
        self.created_by = created_by or "system"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "provider": self.provider,
            "content": self.content,
            "variables": self.variables,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "created_by": self.created_by,
        }


class InfraBuilderService:
    """インフラ構築サービス"""

    def __init__(self):
        self._projects: Dict[str, BuildProject] = {}
        self._pipelines: Dict[str, PipelineRun] = {}
        self._blueprints: Dict[str, Blueprint] = {}
        self._init_demo_data()

    def _init_demo_data(self) -> None:
        """デモ用初期データ"""
        # サンプルブループリント
        bp = Blueprint(
            id="bp-docker-compose-001",
            name="Docker Compose 基本構成",
            provider="docker-compose",
            content="version: '3.8'\nservices:\n  app:\n    image: nginx:alpine\n    ports:\n      - '8080:80'",
            variables={"port": "8080"},
            description="Nginx ベースの基本構成",
        )
        self._blueprints[bp.id] = bp

        bp2 = Blueprint(
            id="bp-terraform-001",
            name="Terraform AWS VPC",
            provider="terraform",
            content='resource "aws_vpc" "main" {\n  cidr_block = "10.0.0.0/16"\n}',
            variables={"cidr_block": "10.0.0.0/16"},
            description="AWS VPC 基本構成",
        )
        self._blueprints[bp2.id] = bp2

        # サンプルプロジェクト
        proj = BuildProject(
            id="proj-001",
            name="Webアプリ基盤構築",
            description="Nginx + Redis のコンテナ基盤",
            target_provider="docker",
            blueprint={"template_id": "bp-docker-compose-001"},
            status=BuildProjectStatus.IN_PROGRESS,
            current_stage=BuildStage.BUILD,
            created_by="demo",
        )
        self._projects[proj.id] = proj

        proj2 = BuildProject(
            id="proj-002",
            name="Kubernetes クラスタ構築",
            description="K8s マニフェストによるデプロイ",
            target_provider="kubernetes",
            status=BuildProjectStatus.DRAFT,
            current_stage=BuildStage.DESIGN,
            created_by="demo",
        )
        self._projects[proj2.id] = proj2

        # サンプルパイプライン実行
        pipe = PipelineRun(
            id="pipe-001",
            project_id="proj-001",
            stages=["design", "build", "deploy", "verify"],
            status=PipelineStatus.SUCCESS,
            current_stage="verify",
            completed_at=datetime.utcnow(),
            logs=[
                "[design] 設計完了",
                "[build] Docker イメージビルド成功",
                "[deploy] デプロイ完了",
                "[verify] ヘルスチェック成功",
            ],
        )
        self._pipelines[pipe.id] = pipe

    def list_projects(
        self,
        status: Optional[BuildProjectStatus] = None,
        provider: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """プロジェクト一覧"""
        result = list(self._projects.values())
        if status:
            result = [p for p in result if p.status == status]
        if provider:
            result = [p for p in result if p.target_provider == provider]
        return [p.to_dict() for p in sorted(result, key=lambda x: x.updated_at, reverse=True)]

    def create_project(
        self,
        name: str,
        description: Optional[str] = None,
        target_provider: str = "docker",
        blueprint: Optional[Dict[str, Any]] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """プロジェクト作成"""
        project_id = f"proj-{uuid.uuid4().hex[:8]}"
        project = BuildProject(
            id=project_id,
            name=name,
            description=description,
            target_provider=target_provider,
            blueprint=blueprint,
            created_by=created_by or "system",
        )
        self._projects[project_id] = project
        return project.to_dict()

    def get_project(self, project_id: str) -> Optional[Dict[str, Any]]:
        """プロジェクト取得"""
        project = self._projects.get(project_id)
        return project.to_dict() if project else None

    def list_blueprints(self, provider: Optional[str] = None) -> List[Dict[str, Any]]:
        """ブループリント一覧"""
        result = list(self._blueprints.values())
        if provider:
            result = [b for b in result if b.provider == provider]
        return [b.to_dict() for b in sorted(result, key=lambda x: x.created_at, reverse=True)]

    def create_blueprint(
        self,
        name: str,
        provider: str,
        content: str,
        variables: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
        created_by: Optional[str] = None,
    ) -> Dict[str, Any]:
        """ブループリント作成"""
        bp_id = f"bp-{uuid.uuid4().hex[:8]}"
        blueprint = Blueprint(
            id=bp_id,
            name=name,
            provider=provider,
            content=content,
            variables=variables,
            description=description,
            created_by=created_by or "system",
        )
        self._blueprints[bp_id] = blueprint
        return blueprint.to_dict()

    def list_pipelines(
        self,
        project_id: Optional[str] = None,
        status: Optional[PipelineStatus] = None,
    ) -> List[Dict[str, Any]]:
        """パイプライン実行一覧"""
        result = list(self._pipelines.values())
        if project_id:
            result = [p for p in result if p.project_id == project_id]
        if status:
            result = [p for p in result if p.status == status]
        return [p.to_dict() for p in sorted(result, key=lambda x: x.started_at, reverse=True)]

    def run_pipeline(
        self,
        project_id: str,
        stages: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """パイプライン実行（シミュレーション）"""
        project = self._projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        pipe_id = f"pipe-{uuid.uuid4().hex[:8]}"
        stage_list = stages or ["design", "build", "deploy", "verify"]

        pipeline = PipelineRun(
            id=pipe_id,
            project_id=project_id,
            stages=stage_list,
            status=PipelineStatus.SUCCESS,  # デモ用に即成功
            current_stage=stage_list[-1],
            logs=[f"[{s}] ステージ完了" for s in stage_list],
        )
        self._pipelines[pipe_id] = pipeline
        return pipeline.to_dict()

    def get_dashboard(self) -> Dict[str, Any]:
        """ダッシュボードサマリー"""
        projects = list(self._projects.values())
        return {
            "total_projects": len(projects),
            "in_progress": len([p for p in projects if p.status == BuildProjectStatus.IN_PROGRESS]),
            "completed": len([p for p in projects if p.status == BuildProjectStatus.COMPLETED]),
            "draft": len([p for p in projects if p.status == BuildProjectStatus.DRAFT]),
            "total_blueprints": len(self._blueprints),
            "total_pipeline_runs": len(self._pipelines),
            "providers": ["docker", "kubernetes", "terraform", "docker-compose"],
        }
