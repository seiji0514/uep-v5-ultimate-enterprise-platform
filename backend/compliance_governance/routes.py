"""
コンプライアンス・ガバナンス系 API
規制対応、監査
認証不要でデモ用サンプルデータを返す
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/compliance-governance", tags=["コンプライアンス・ガバナンス系"])


def _regulatory_items() -> List[Dict[str, Any]]:
    return [
        {
            "id": "reg-001",
            "regulation": "個人情報保護法",
            "status": "対応済",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),
            "compliance_score": 98,
            "scope": "全社",
        },
        {
            "id": "reg-002",
            "regulation": "金融商品取引法",
            "status": "監査中",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat(),
            "compliance_score": 85,
            "scope": "金融部門",
        },
        {
            "id": "reg-003",
            "regulation": "ISO27001",
            "status": "要対応",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=90)).isoformat(),
            "compliance_score": 72,
            "scope": "全社",
        },
        {
            "id": "reg-004",
            "regulation": "GDPR",
            "status": "対応済",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=45)).isoformat(),
            "compliance_score": 95,
            "scope": "EU向け",
        },
        {
            "id": "reg-005",
            "regulation": "SOC2",
            "status": "監査中",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=10)).isoformat(),
            "compliance_score": 88,
            "scope": "クラウド",
        },
        {
            "id": "reg-006",
            "regulation": "PCI-DSS",
            "status": "対応済",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=60)).isoformat(),
            "compliance_score": 96,
            "scope": "決済",
        },
        {
            "id": "reg-007",
            "regulation": "医薬品医療機器法",
            "status": "監査中",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=15)).isoformat(),
            "compliance_score": 82,
            "scope": "医療部門",
        },
        {
            "id": "reg-008",
            "regulation": "電子帳簿保存法",
            "status": "対応済",
            "last_audit": (datetime.now(timezone.utc) - timedelta(days=20)).isoformat(),
            "compliance_score": 94,
            "scope": "経理",
        },
    ]


def _audit_logs() -> List[Dict[str, Any]]:
    return [
        {
            "id": "aud-001",
            "action": "データアクセス",
            "user": "admin",
            "resource": "顧客DB",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(),
        },
        {
            "id": "aud-002",
            "action": "設定変更",
            "user": "ops",
            "resource": "セキュリティポリシー",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat(),
        },
        {
            "id": "aud-003",
            "action": "権限昇格",
            "user": "admin",
            "resource": "RBAC",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=5)).isoformat(),
        },
        {
            "id": "aud-004",
            "action": "ログエクスポート",
            "user": "auditor",
            "resource": "監査ログ",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=30)).isoformat(),
        },
        {
            "id": "aud-005",
            "action": "API呼び出し",
            "user": "api-client",
            "resource": "決済API",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=5)).isoformat(),
        },
        {
            "id": "aud-006",
            "action": "ログイン失敗",
            "user": "unknown",
            "resource": "認証",
            "result": "拒否",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=15)).isoformat(),
        },
        {
            "id": "aud-007",
            "action": "データ削除",
            "user": "admin",
            "resource": "アーカイブ",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
        },
        {
            "id": "aud-008",
            "action": "ポリシー承認",
            "user": "compliance",
            "resource": "AI利用ガイドライン",
            "result": "許可",
            "timestamp": (datetime.now(timezone.utc) - timedelta(minutes=45)).isoformat(),
        },
    ]


def _governance_policies() -> List[Dict[str, Any]]:
    return [
        {
            "id": "pol-001",
            "name": "AI利用ガイドライン",
            "version": "2.1",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            "owner": "AI推進室",
        },
        {
            "id": "pol-002",
            "name": "データ保持ポリシー",
            "version": "1.0",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=30)).isoformat(),
            "owner": "法務",
        },
        {
            "id": "pol-003",
            "name": "アクセス制御基準",
            "version": "3.0",
            "status": "改定中",
            "updated": (datetime.now(timezone.utc) - timedelta(days=3)).isoformat(),
            "owner": "セキュリティ",
        },
        {
            "id": "pol-004",
            "name": "インシデント対応手順",
            "version": "1.2",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=14)).isoformat(),
            "owner": "運用",
        },
        {
            "id": "pol-005",
            "name": "BCP",
            "version": "2.0",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=60)).isoformat(),
            "owner": "経営企画",
        },
        {
            "id": "pol-006",
            "name": "リモートワーク基準",
            "version": "1.5",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=45)).isoformat(),
            "owner": "人事",
        },
        {
            "id": "pol-007",
            "name": "クラウド利用ポリシー",
            "version": "2.0",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=21)).isoformat(),
            "owner": "インフラ",
        },
        {
            "id": "pol-008",
            "name": "サプライヤー管理基準",
            "version": "1.0",
            "status": "有効",
            "updated": (datetime.now(timezone.utc) - timedelta(days=90)).isoformat(),
            "owner": "調達",
        },
    ]


def _audit_findings() -> List[Dict[str, Any]]:
    return [
        {
            "id": "find-001",
            "severity": "高",
            "description": "ログ保持期間不足",
            "status": "対応中",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=14)).isoformat(),
            "owner": "運用",
        },
        {
            "id": "find-002",
            "severity": "中",
            "description": "パスワードポリシー未適用",
            "status": "未対応",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "owner": "セキュリティ",
        },
        {
            "id": "find-003",
            "severity": "低",
            "description": "ドキュメント更新遅延",
            "status": "対応済",
            "due_date": (datetime.now(timezone.utc) - timedelta(days=7)).isoformat(),
            "owner": "各部門",
        },
        {
            "id": "find-004",
            "severity": "中",
            "description": "MFA未設定アカウントあり",
            "status": "対応中",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=21)).isoformat(),
            "owner": "IT",
        },
        {
            "id": "find-005",
            "severity": "低",
            "description": "監査証跡の欠落",
            "status": "未対応",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=45)).isoformat(),
            "owner": "開発",
        },
        {
            "id": "find-006",
            "severity": "高",
            "description": "脆弱性スキャン未実施",
            "status": "対応中",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=7)).isoformat(),
            "owner": "セキュリティ",
        },
        {
            "id": "find-007",
            "severity": "中",
            "description": "バックアップテスト未実施",
            "status": "未対応",
            "due_date": (datetime.now(timezone.utc) + timedelta(days=30)).isoformat(),
            "owner": "運用",
        },
        {
            "id": "find-008",
            "severity": "低",
            "description": "アクセス権限の棚卸し",
            "status": "対応済",
            "due_date": (datetime.now(timezone.utc) - timedelta(days=14)).isoformat(),
            "owner": "人事",
        },
    ]


@router.get("/regulatory-items")
async def get_regulatory():
    return {"items": _regulatory_items(), "total": len(_regulatory_items())}


@router.get("/audit-logs")
async def get_audit_logs():
    return {"items": _audit_logs(), "total": len(_audit_logs())}


@router.get("/governance-policies")
async def get_policies():
    return {"items": _governance_policies(), "total": len(_governance_policies())}


@router.get("/audit-findings")
async def get_findings():
    return {"items": _audit_findings(), "total": len(_audit_findings())}


@router.get("/dashboard")
async def get_dashboard():
    return {
        "regulatory_compliance_avg": sum(
            r["compliance_score"] for r in _regulatory_items()
        )
        // len(_regulatory_items())
        if _regulatory_items()
        else 0,
        "audit_findings_open": len(
            [f for f in _audit_findings() if f["status"] != "対応済"]
        ),
        "policies_count": len(_governance_policies()),
        "audit_logs_today": len(_audit_logs()),
    }
