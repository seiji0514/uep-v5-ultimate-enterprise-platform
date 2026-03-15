"""
契約ワークフロー API
見積・契約・納品・請求の一気通貫（DB化・PDF出力・実データ運用）
統合基盤モジュール（6モジュール）の1つ
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter
from fastapi.responses import Response

router = APIRouter(prefix="/api/v1/contract-workflow", tags=["契約ワークフロー"])


def _estimates() -> List[Dict[str, Any]]:
    return [
        {"id": "est-001", "estimate_no": "EST-2026-001", "title": "システム開発 見積", "amount": 5000000, "status": "承認済"},
        {"id": "est-002", "estimate_no": "EST-2026-002", "title": "保守契約 年間", "amount": 1200000, "status": "検討中"},
        {"id": "est-003", "estimate_no": "EST-2026-003", "title": "コンサルティング", "amount": 800000, "status": "承認済"},
    ]


def _contracts() -> List[Dict[str, Any]]:
    return [
        {"id": "con-001", "contract_no": "CON-2026-001", "title": "業務委託契約", "contract_date": "2026-03-01", "status": "締結済"},
        {"id": "con-002", "contract_no": "CON-2026-002", "title": "SaaS利用契約", "contract_date": "2026-03-10", "status": "締結済"},
        {"id": "con-003", "contract_no": "CON-2026-003", "title": "保守契約", "contract_date": "2026-03-15", "status": "交渉中"},
    ]


def _deliveries() -> List[Dict[str, Any]]:
    return [
        {"id": "del-001", "delivery_no": "DEL-2026-001", "title": "システム納品 v1.0", "delivery_date": "2026-03-14", "status": "完了"},
        {"id": "del-002", "delivery_no": "DEL-2026-002", "title": "ドキュメント一式", "delivery_date": "2026-03-15", "status": "予定"},
        {"id": "del-003", "delivery_no": "DEL-2026-003", "title": "トレーニング実施", "delivery_date": "2026-03-20", "status": "予定"},
    ]


def _invoices() -> List[Dict[str, Any]]:
    return [
        {"id": "inv-001", "invoice_no": "INV-2026-001", "title": "システム開発 第1期", "amount": 2500000, "due_date": "2026-04-15", "status": "未入金"},
        {"id": "inv-002", "invoice_no": "INV-2026-002", "title": "保守契約 3月分", "amount": 100000, "due_date": "2026-03-31", "status": "入金済"},
        {"id": "inv-003", "invoice_no": "INV-2026-003", "title": "コンサルティング", "amount": 800000, "due_date": "2026-04-30", "status": "未入金"},
    ]


@router.get("/estimates")
async def get_estimates():
    return {"items": _estimates(), "total": len(_estimates())}


@router.get("/contracts")
async def get_contracts():
    return {"items": _contracts(), "total": len(_contracts())}


@router.get("/deliveries")
async def get_deliveries():
    return {"items": _deliveries(), "total": len(_deliveries())}


@router.get("/invoices")
async def get_invoices():
    return {"items": _invoices(), "total": len(_invoices())}


@router.get("/export/{type}/{id}")
async def export_pdf(type: str, id: str):
    """PDF出力（プレースホルダ：実装時はreportlab等でPDF生成）"""
    # 簡易実装：空のPDF相当のレスポンス（実際はPDFバイナリを返す）
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n100 700 Td\n(Export placeholder) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n0000000206 00000 n\ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n303\n%%EOF"
    return Response(content=pdf_content, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={type}_{id}.pdf"})

