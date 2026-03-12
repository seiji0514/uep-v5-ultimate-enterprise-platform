"""
一元化サンプルデータ - MLOps から Level 5 グローバルエンタープライズまで

デモ用に、共通プロジェクトIDで紐づいたサンプルデータを各モジュールに投入。
物理的にリアルなデモ体験を提供する。
"""
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

# 共通プロジェクトID（一元化のキー）
UNIFIED_PROJECT_ID = "uep-demo-unified"
UNIFIED_PROJECT_NAME = "UEP推論最適化基盤"


def init_unified_demo_data() -> None:
    """MLOps〜Level 5 まで一元化したサンプルデータを投入"""
    try:
        _seed_cloud_infra()
        _seed_mlops()
        _seed_infra_builder()
        _seed_security_center()
        _seed_idop()
        logger.info("一元化サンプルデータの投入が完了しました")
    except Exception as e:
        logger.warning(f"サンプルデータ投入でエラー（続行）: {e}")


def _seed_cloud_infra() -> None:
    """クラウドインフラ・オーケストレーション・IaC にサンプルデータ投入"""
    from cloud_infra.infrastructure import (
        InfrastructureResource,
        ResourceStatus,
        ResourceType,
        infrastructure_manager,
    )
    from cloud_infra.iac import IaCProvider, IaCTemplate, iac_manager
    from cloud_infra.orchestration import (
        Deployment,
        DeploymentStatus,
        OrchestrationPlatform,
        orchestration_manager,
    )

    # 既にデータがある場合はスキップ
    if infrastructure_manager.list_resources():
        return

    now = datetime.utcnow()
    base_tags = {"project": UNIFIED_PROJECT_ID, "env": "demo"}

    # インフラリソース（ap-northeast-1 = Level 5 東京リージョンと連携）
    resources = [
        InfrastructureResource(
            id="res-uep-demo-001",
            name="uep-inference-eks-cluster",
            resource_type=ResourceType.CONTAINER,
            provider="aws",
            region="ap-northeast-1",
            status=ResourceStatus.RUNNING,
            config={"node_count": 3, "instance_type": "m5.large"},
            created_at=now - timedelta(days=7),
            updated_at=now,
            tags={**base_tags, "level": "5"},
        ),
        InfrastructureResource(
            id="res-uep-demo-002",
            name="uep-mlops-s3-bucket",
            resource_type=ResourceType.STORAGE,
            provider="aws",
            region="ap-northeast-1",
            status=ResourceStatus.RUNNING,
            config={"storage_class": "STANDARD"},
            created_at=now - timedelta(days=14),
            updated_at=now,
            tags={**base_tags, "purpose": "model-artifacts"},
        ),
        InfrastructureResource(
            id="res-uep-demo-003",
            name="uep-api-gateway",
            resource_type=ResourceType.NETWORK,
            provider="aws",
            region="ap-northeast-1",
            status=ResourceStatus.RUNNING,
            config={"type": "Kong"},
            created_at=now - timedelta(days=5),
            updated_at=now,
            tags={**base_tags, "level": "5"},
        ),
    ]

    for r in resources:
        infrastructure_manager._resources[r.id] = r

    # IaCテンプレート
    templates = [
        IaCTemplate(
            id="tpl-uep-demo-001",
            name="UEP EKS クラスタ（Level 5 東京）",
            description=f"{UNIFIED_PROJECT_NAME}用 EKS テンプレート",
            provider=IaCProvider.TERRAFORM,
            template_content='resource "aws_eks_cluster" "uep" {\n  name = "uep-inference"\n  role_arn = aws_iam_role.eks.arn\n}',
            variables={"region": "ap-northeast-1"},
            created_at=now - timedelta(days=10),
            updated_at=now,
            created_by="demo",
        ),
    ]
    for t in templates:
        iac_manager._templates[t.id] = t

    # デプロイメント（Kubernetes）
    deployments = [
        Deployment(
            id="dep-uep-demo-001",
            name="uep-inference-api",
            platform=OrchestrationPlatform.KUBERNETES,
            image="uep/inference-api:v1.2",
            replicas=3,
            status=DeploymentStatus.RUNNING,
            config={"cpu": "500m", "memory": "512Mi"},
            created_at=now - timedelta(days=3),
            updated_at=now,
            namespace="uep-mlops",
        ),
        Deployment(
            id="dep-uep-demo-002",
            name="uep-prometheus",
            platform=OrchestrationPlatform.KUBERNETES,
            image="prom/prometheus:v2.45",
            replicas=2,
            status=DeploymentStatus.RUNNING,
            config={},
            created_at=now - timedelta(days=5),
            updated_at=now,
            namespace="uep-monitoring",
        ),
    ]
    for d in deployments:
        orchestration_manager._deployments[d.id] = d


def _seed_infra_builder() -> None:
    """インフラ構築専用に一元化プロジェクトを追加"""
    from infra_builder.routes import infra_builder_service
    from infra_builder.services import BuildProject, BuildProjectStatus, BuildStage

    service = infra_builder_service
    if any(p.name == UNIFIED_PROJECT_NAME for p in service._projects.values()):
        return

    now = datetime.utcnow()
    proj = BuildProject(
        id="proj-uep-unified",
        name=UNIFIED_PROJECT_NAME,
        description="MLOps推論モデル→クラウドインフラ→Level 5東京リージョンまで一元化",
        target_provider="kubernetes",
        blueprint={"template_id": "tpl-uep-demo-001", "region": "ap-northeast-1"},
        status=BuildProjectStatus.IN_PROGRESS,
        current_stage=BuildStage.DEPLOY,
        created_at=now - timedelta(days=5),
        updated_at=now,
        created_by="demo",
    )
    service._projects[proj.id] = proj


def _seed_mlops() -> None:
    """MLOps（実験追跡・モデルレジストリ・パイプライン）にサンプルデータ投入"""
    from mlops.experiment_tracking import Experiment, experiment_tracker
    from mlops.model_registry import MLModel, ModelStatus, ModelVersion, model_registry
    from mlops.pipeline import MLPipeline, PipelineStage, PipelineStatus, pipeline_executor

    now = datetime.utcnow()

    # パイプライン（企業デモ用・空だと信用されない）
    if not pipeline_executor._pipelines:
        pipe1 = MLPipeline(
            id="pipe-uep-demo-001",
            name=f"{UNIFIED_PROJECT_NAME} 学習パイプライン",
            description="推論モデル v1.2 の学習・評価・デプロイまで自動化",
            stages=[
                PipelineStage(id="stage-1", name="データ前処理", stage_type="data_preprocessing", config={"batch_size": 32}),
                PipelineStage(id="stage-2", name="学習", stage_type="training", config={"epochs": 10}, dependencies=["stage-1"]),
                PipelineStage(id="stage-3", name="評価", stage_type="evaluation", config={}, dependencies=["stage-2"]),
                PipelineStage(id="stage-4", name="デプロイ", stage_type="deployment", config={"target": "production"}, dependencies=["stage-3"]),
            ],
            status=PipelineStatus.SUCCESS,
            created_at=now - timedelta(days=7),
            updated_at=now,
            created_by="demo",
        )
        pipe2 = MLPipeline(
            id="pipe-uep-demo-002",
            name="A/Bテスト モデル比較パイプライン",
            description="v1.1 vs v1.2 推論性能比較",
            stages=[
                PipelineStage(id="s1", name="モデル読み込み", stage_type="data_preprocessing", config={}),
                PipelineStage(id="s2", name="推論比較", stage_type="evaluation", config={}, dependencies=["s1"]),
            ],
            status=PipelineStatus.RUNNING,
            created_at=now - timedelta(days=3),
            updated_at=now,
            created_by="demo",
        )
        pipeline_executor._pipelines[pipe1.id] = pipe1
        pipeline_executor._pipelines[pipe2.id] = pipe2
    base_tags = [UNIFIED_PROJECT_ID, "inference-optimization"]

    # 既にデータがある場合はスキップ
    if experiment_tracker.list_experiments():
        return

    # 実験
    experiments = [
        Experiment(
            id="exp-uep-demo-001",
            name="推論レイテンシ最適化",
            description=f"{UNIFIED_PROJECT_NAME} - レイテンシ50%削減を目標",
            parameters={"batch_size": 32, "model_type": "transformer"},
            metrics={"latency_ms": 8.5, "throughput": 1200, "accuracy": 0.95},
            tags=base_tags,
            status="completed",
            created_at=now - timedelta(days=14),
            updated_at=now - timedelta(days=7),
            created_by="demo",
            artifacts=["s3://uep-mlops/models/sentiment-v1.2"],
        ),
        Experiment(
            id="exp-uep-demo-002",
            name="A/Bテスト モデル比較",
            description="v1.1 vs v1.2 推論性能比較",
            parameters={"control": "v1.1", "treatment": "v1.2"},
            metrics={"latency_improvement": 0.52, "p_value": 0.02},
            tags=base_tags,
            status="completed",
            created_at=now - timedelta(days=10),
            updated_at=now - timedelta(days=5),
            created_by="demo",
            artifacts=[],
        ),
    ]
    for e in experiments:
        experiment_tracker._experiments[e.id] = e

    # モデルレジストリ
    if model_registry._models:
        return

    model = MLModel(
        id="model-uep-demo-001",
        name="sentiment-inference-v1",
        description=f"{UNIFIED_PROJECT_NAME} - 推論用モデル",
        model_type="classification",
        framework="pytorch",
        versions=[
            ModelVersion(
                version="1.2",
                model_path="s3://uep-mlops/models/sentiment-v1.2",
                metrics={"latency_ms": 8.5, "accuracy": 0.95},
                status=ModelStatus.PRODUCTION,
                created_at=now - timedelta(days=7),
                created_by="demo",
                metadata={"region": "ap-northeast-1", "level": "5"},
            ),
        ],
        current_version="1.2",
        created_at=now - timedelta(days=14),
        updated_at=now,
        created_by="demo",
    )
    model_registry._models[model.id] = model


def _seed_security_center() -> None:
    """セキュリティコマンドセンターにサンプルデータ投入"""
    from security_center.monitoring import SecurityEvent, ThreatLevel, security_monitor
    from security_center.incident_response import Incident, IncidentSeverity, IncidentStatus, incident_response

    now = datetime.utcnow()

    if not security_monitor._events:
        events = [
            SecurityEvent(
                id="evt-demo-001",
                event_type="auth_failure",
                threat_level=ThreatLevel.MEDIUM,
                source="192.168.1.100",
                target="api-gateway",
                description="認証失敗が5分間に10回検出。ブルートフォース攻撃の疑い",
                timestamp=now - timedelta(hours=2),
                status="investigating",
            ),
            SecurityEvent(
                id="evt-demo-002",
                event_type="access_anomaly",
                threat_level=ThreatLevel.LOW,
                source="10.0.1.50",
                target="data-lake",
                description="通常と異なるアクセスパターンを検出",
                timestamp=now - timedelta(hours=5),
                status="resolved",
            ),
            SecurityEvent(
                id="evt-demo-003",
                event_type="intrusion",
                threat_level=ThreatLevel.HIGH,
                source="203.0.113.42",
                target="dmz-web",
                description="既知の脆弱性を突いた侵入試行。WAFでブロック済み",
                timestamp=now - timedelta(minutes=30),
                status="open",
            ),
            SecurityEvent(
                id="evt-demo-004",
                event_type="data_exfiltration",
                threat_level=ThreatLevel.CRITICAL,
                source="内部ネットワーク",
                target="外部IP",
                description="大量データ送信を検知。DLPアラート発報",
                timestamp=now - timedelta(minutes=15),
                status="investigating",
            ),
        ]
        for e in events:
            security_monitor._events[e.id] = e

    if not incident_response._incidents:
        incidents = [
            Incident(
                id="inc-demo-001",
                title="API認証エラー多発",
                description="JWT検証失敗が閾値を超過。調査中",
                severity=IncidentSeverity.MEDIUM,
                status=IncidentStatus.INVESTIGATING,
                affected_systems=["api-gateway", "auth-service"],
                assigned_to="sec-team",
                created_at=now - timedelta(hours=3),
                updated_at=now,
            ),
            Incident(
                id="inc-demo-002",
                title="異常ログイン試行",
                description="海外IPからのログイン試行を検知。ブロック済み",
                severity=IncidentSeverity.LOW,
                status=IncidentStatus.RESOLVED,
                affected_systems=["auth-service"],
                resolved_at=now - timedelta(hours=1),
                resolution="IPブロックリストに追加",
                created_at=now - timedelta(hours=6),
                updated_at=now,
            ),
        ]
        for i in incidents:
            incident_response._incidents[i.id] = i


def _seed_idop() -> None:
    """IDOP（CI/CD・アプリケーション）にサンプルデータ投入"""
    from idop.cicd import CICDPipelineModel, CICDStatus, PipelineStage, cicd_pipeline
    from idop.devops import Application, Environment, devops_manager

    now = datetime.utcnow()

    if not cicd_pipeline._pipelines:
        pipes = [
            CICDPipelineModel(
                id="cicd-demo-001",
                name=f"{UNIFIED_PROJECT_NAME} CI/CD",
                repository="https://github.com/uep/uep-inference-api",
                branch="main",
                stages=[PipelineStage.BUILD, PipelineStage.TEST, PipelineStage.DEPLOY],
                status=CICDStatus.SUCCESS,
                created_at=now - timedelta(days=5),
                updated_at=now,
                created_by="demo",
            ),
            CICDPipelineModel(
                id="cicd-demo-002",
                name="UEP フロントエンド ビルド",
                repository="https://github.com/uep/uep-frontend",
                branch="main",
                stages=[PipelineStage.BUILD, PipelineStage.TEST],
                status=CICDStatus.RUNNING,
                created_at=now - timedelta(days=2),
                updated_at=now,
                created_by="demo",
            ),
        ]
        for p in pipes:
            cicd_pipeline._pipelines[p.id] = p

    if not devops_manager._applications:
        apps = [
            Application(
                id="app-demo-001",
                name="uep-inference-api",
                description="推論API マイクロサービス",
                repository="https://github.com/uep/uep-inference-api",
                environments=[Environment.DEVELOPMENT, Environment.STAGING, Environment.PRODUCTION],
                current_version="v1.2.0",
                created_at=now - timedelta(days=14),
                updated_at=now,
                created_by="demo",
            ),
            Application(
                id="app-demo-002",
                name="uep-dashboard",
                description="統合ダッシュボード",
                repository="https://github.com/uep/uep-dashboard",
                environments=[Environment.DEVELOPMENT, Environment.STAGING],
                current_version="v2.0.1",
                created_at=now - timedelta(days=7),
                updated_at=now,
                created_by="demo",
            ),
        ]
        for a in apps:
            devops_manager._applications[a.id] = a
