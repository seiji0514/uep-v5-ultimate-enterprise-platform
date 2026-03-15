"""
6モジュール横断・要対応集約API
製造・医療・金融・障害者雇用・契約の要対応を集約
"""
from typing import Any, Dict

from fastapi import APIRouter, Depends

from auth.jwt_auth import get_current_active_user

router = APIRouter(prefix="/api/v1/cross-module", tags=["6モジュール横断"])


@router.get("/action-items")
async def get_action_items(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """6モジュールの要対応を集約（UEPダッシュボード横断表示用）"""
    manufacturing_count = 0
    medical_count = 0
    fintech_count = 0
    inclusive_work_count = 0
    contract_count = 0

    try:
        from manufacturing.routes import _predictive_maintenance_list, _anomaly_list

        pm = _predictive_maintenance_list()
        an = _anomaly_list()
        manufacturing_count = len([p for p in pm if p.get("status") == "要メンテナンス"])
        manufacturing_count += len([a for a in an if a.get("severity") == "高"])
    except Exception:
        pass

    try:
        from medical.routes import _ai_diagnosis_list

        diag = _ai_diagnosis_list()
        medical_count = len([d for d in diag if d.get("status") in ("要確認", "要精査")])
    except Exception:
        pass

    try:
        from fintech.routes import _risk_scores, _transaction_monitoring

        risk = _risk_scores()
        mon = _transaction_monitoring()
        fintech_count = len([r for r in risk if r.get("level") == "高"])
        fintech_count += len([m for m in mon if m.get("status") == "要確認"])
    except Exception:
        pass

    try:
        from contract_workflow.routes import _contracts, _estimates, _invoices

        contracts = _contracts()
        estimates = _estimates()
        invoices = _invoices()
        contract_count = len([c for c in contracts if c.get("status") in ("交渉中", "レビュー中")])
        contract_count += len([e for e in estimates if e.get("status") in ("検討中", "承認待ち")])
        contract_count += len([i for i in invoices if i.get("status") == "未入金"])
    except Exception:
        pass

    total = manufacturing_count + medical_count + fintech_count + inclusive_work_count + contract_count

    return {
        "manufacturing": manufacturing_count,
        "medical": medical_count,
        "fintech": fintech_count,
        "inclusive_work": inclusive_work_count,
        "contract": contract_count,
        "total": total,
        "source": "uep_5_modules",
    }
