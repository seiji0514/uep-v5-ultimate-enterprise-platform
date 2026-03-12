"""
インフラ・運用系 API（SIer・クラウドベンダー向け）
IaC、オーケストレーション、監視、最適化
認証不要でデモ用サンプルデータを返す
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/infra-ops", tags=["インフラ・運用系"])


def _iac_projects() -> List[Dict[str, Any]]:
    return [
        {"id": "iac-001", "name": "EKS本番クラスタ", "provider": "AWS", "status": "デプロイ済", "last_deploy": (datetime.utcnow() - timedelta(hours=2)).isoformat(), "region": "ap-northeast-1"},
        {"id": "iac-002", "name": "VPC基盤", "provider": "Terraform", "status": "適用中", "last_deploy": (datetime.utcnow() - timedelta(days=1)).isoformat(), "region": "ap-northeast-1"},
        {"id": "iac-003", "name": "監視基盤", "provider": "AWS", "status": "ドリフト検知", "last_deploy": (datetime.utcnow() - timedelta(days=3)).isoformat(), "region": "ap-northeast-1"},
        {"id": "iac-004", "name": "RDS本番DB", "provider": "Terraform", "status": "デプロイ済", "last_deploy": (datetime.utcnow() - timedelta(hours=12)).isoformat(), "region": "ap-northeast-1"},
        {"id": "iac-005", "name": "Lambda関数群", "provider": "AWS CDK", "status": "適用中", "last_deploy": (datetime.utcnow() - timedelta(hours=6)).isoformat(), "region": "ap-northeast-1"},
        {"id": "iac-006", "name": "CloudFront配信", "provider": "Terraform", "status": "デプロイ済", "last_deploy": (datetime.utcnow() - timedelta(days=5)).isoformat(), "region": "global"},
        {"id": "iac-007", "name": "WAFルールセット", "provider": "AWS", "status": "適用中", "last_deploy": (datetime.utcnow() - timedelta(hours=24)).isoformat(), "region": "ap-northeast-1"},
        {"id": "iac-008", "name": "SQS/SNS基盤", "provider": "Terraform", "status": "ドリフト検知", "last_deploy": (datetime.utcnow() - timedelta(days=7)).isoformat(), "region": "ap-northeast-1"},
    ]


def _orchestration_deployments() -> List[Dict[str, Any]]:
    return [
        {"id": "dep-001", "app": "api-gateway", "env": "production", "status": "Running", "replicas": 3, "updated": (datetime.utcnow() - timedelta(minutes=30)).isoformat(), "namespace": "prod"},
        {"id": "dep-002", "app": "worker-queue", "env": "production", "status": "Running", "replicas": 5, "updated": (datetime.utcnow() - timedelta(hours=1)).isoformat(), "namespace": "prod"},
        {"id": "dep-003", "app": "batch-job", "env": "staging", "status": "Pending", "replicas": 1, "updated": (datetime.utcnow() - timedelta(minutes=5)).isoformat(), "namespace": "staging"},
        {"id": "dep-004", "app": "frontend-spa", "env": "production", "status": "Running", "replicas": 2, "updated": (datetime.utcnow() - timedelta(minutes=15)).isoformat(), "namespace": "prod"},
        {"id": "dep-005", "app": "analytics-service", "env": "staging", "status": "Running", "replicas": 1, "updated": (datetime.utcnow() - timedelta(hours=2)).isoformat(), "namespace": "staging"},
        {"id": "dep-006", "app": "auth-service", "env": "production", "status": "Running", "replicas": 2, "updated": (datetime.utcnow() - timedelta(hours=4)).isoformat(), "namespace": "prod"},
        {"id": "dep-007", "app": "report-generator", "env": "staging", "status": "Pending", "replicas": 1, "updated": (datetime.utcnow() - timedelta(minutes=20)).isoformat(), "namespace": "staging"},
        {"id": "dep-008", "app": "cache-proxy", "env": "production", "status": "Running", "replicas": 4, "updated": (datetime.utcnow() - timedelta(minutes=45)).isoformat(), "namespace": "prod"},
    ]


def _monitoring_alerts() -> List[Dict[str, Any]]:
    return [
        {"id": "alt-001", "service": "api-gateway", "metric": "CPU使用率", "value": 92, "threshold": 80, "severity": "高", "status": "未対応", "source": "CloudWatch"},
        {"id": "alt-002", "service": "db-primary", "metric": "接続数", "value": 450, "threshold": 500, "severity": "中", "status": "監視中", "source": "RDS"},
        {"id": "alt-003", "service": "cache", "metric": "メモリ使用率", "value": 78, "threshold": 85, "severity": "低", "status": "対応済", "source": "ElastiCache"},
        {"id": "alt-004", "service": "worker-queue", "metric": "キュー滞留", "value": 1250, "threshold": 1000, "severity": "高", "status": "未対応", "source": "SQS"},
        {"id": "alt-005", "service": "api-gateway", "metric": "レイテンシp99", "value": 850, "threshold": 500, "severity": "中", "status": "監視中", "source": "X-Ray"},
        {"id": "alt-006", "service": "frontend-spa", "metric": "エラー率", "value": 0.8, "threshold": 0.5, "severity": "中", "status": "未対応", "source": "CloudWatch"},
        {"id": "alt-007", "service": "auth-service", "metric": "認証失敗", "value": 15, "threshold": 10, "severity": "高", "status": "未対応", "source": "Prometheus"},
        {"id": "alt-008", "service": "analytics-service", "metric": "ディスク使用率", "value": 88, "threshold": 90, "severity": "低", "status": "監視中", "source": "Grafana"},
    ]


def _optimization_recommendations() -> List[Dict[str, Any]]:
    return [
        {"id": "opt-001", "type": "FinOps", "resource": "EC2-m5.large", "saving_estimate": 12000, "action": "リザーブドインスタンス検討", "priority": "高"},
        {"id": "opt-002", "type": "スケール", "resource": "worker-queue", "saving_estimate": 0, "action": "夜間スケールダウン推奨", "priority": "中"},
        {"id": "opt-003", "type": "ストレージ", "resource": "S3-archive", "saving_estimate": 5000, "action": "Glacier移行推奨", "priority": "中"},
        {"id": "opt-004", "type": "FinOps", "resource": "RDS-db.t3.medium", "saving_estimate": 18000, "action": "RDSリザーブド検討", "priority": "高"},
        {"id": "opt-005", "type": "ネットワーク", "resource": "NAT Gateway", "saving_estimate": 8000, "action": "VPC Endpoint検討", "priority": "高"},
        {"id": "opt-006", "type": "FinOps", "resource": "Lambda-Provisioned", "saving_estimate": 3500, "action": "Provisioned Concurrency見直し", "priority": "低"},
        {"id": "opt-007", "type": "キャッシュ", "resource": "ElastiCache", "saving_estimate": 6000, "action": "ノードタイプダウングレード検討", "priority": "中"},
    ]


@router.get("/iac-projects")
async def get_iac_projects():
    return {"items": _iac_projects(), "total": len(_iac_projects())}


@router.get("/orchestration-deployments")
async def get_orchestration():
    return {"items": _orchestration_deployments(), "total": len(_orchestration_deployments())}


@router.get("/monitoring-alerts")
async def get_monitoring_alerts():
    return {"items": _monitoring_alerts(), "total": len(_monitoring_alerts())}


@router.get("/optimization-recommendations")
async def get_optimization():
    return {"items": _optimization_recommendations(), "total": len(_optimization_recommendations())}


@router.get("/dashboard")
async def get_dashboard():
    return {
        "iac_projects": len(_iac_projects()),
        "deployments": len(_orchestration_deployments()),
        "alerts_open": len([a for a in _monitoring_alerts() if a["status"] != "対応済"]),
        "optimization_savings": sum(r["saving_estimate"] for r in _optimization_recommendations()),
    }
