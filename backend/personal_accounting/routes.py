"""
個人会計API（freee・マネーフォワード風）
"""
from datetime import date
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from auth.jwt_auth import get_current_active_user

from .expense_categories import (
    ALL_CATEGORIES,
    get_expense_judgment,
    suggest_category,
)
from .models import ExpenseCreate, IncomeCreate
from .store import (
    add_expense,
    add_income,
    delete_expense,
    delete_income,
    get_dashboard_summary,
    get_expenses,
    get_income,
    get_monthly_summary,
)

router = APIRouter(prefix="/api/v1/personal-accounting", tags=["個人会計"])


@router.get("/categories")
async def list_categories(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """経費カテゴリ一覧（経費判定付き）"""
    return {
        "categories": [
            {"id": k, "name": v["name"], "is_expense": v["is_expense"], "note": v.get("note", "")}
            for k, v in ALL_CATEGORIES.items()
        ]
    }


@router.get("/categories/suggest")
async def suggest_categories(
    q: str = Query(..., min_length=1),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """キーワードからカテゴリを推測"""
    return {"suggestions": suggest_category(q)}


@router.get("/categories/{category_id}/judgment")
async def get_category_judgment(
    category_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """カテゴリの経費判定"""
    return get_expense_judgment(category_id)


@router.get("/dashboard")
async def get_dashboard(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ダッシュボードサマリ"""
    return get_dashboard_summary()


@router.get("/expenses")
async def list_expenses(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """経費一覧"""
    return {"items": get_expenses(year, month), "total": len(get_expenses(year, month))}


@router.post("/expenses")
async def create_expense(
    body: ExpenseCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """経費を登録"""
    item = add_expense(
        date_str=body.date.isoformat(),
        category_id=body.category_id,
        amount=body.amount,
        description=body.description,
        memo=body.memo,
    )
    return item


@router.delete("/expenses/{expense_id}")
async def remove_expense(
    expense_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """経費を削除"""
    if not delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "deleted"}


@router.get("/income")
async def list_income(
    year: Optional[int] = Query(None),
    month: Optional[int] = Query(None),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """売上一覧"""
    return {"items": get_income(year, month), "total": len(get_income(year, month))}


@router.post("/income")
async def create_income(
    body: IncomeCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """売上を登録"""
    item = add_income(
        date_str=body.date.isoformat(),
        amount=body.amount,
        description=body.description,
        client_name=body.client_name,
        memo=body.memo,
    )
    return item


@router.delete("/income/{income_id}")
async def remove_income(
    income_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """売上を削除"""
    if not delete_income(income_id):
        raise HTTPException(status_code=404, detail="Income not found")
    return {"message": "deleted"}


@router.get("/summary/monthly")
async def get_monthly(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """月次サマリ"""
    return get_monthly_summary(year, month)
