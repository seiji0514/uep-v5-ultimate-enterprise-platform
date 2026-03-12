"""個人会計のPydanticモデル"""
from datetime import date
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class ExpenseCreate(BaseModel):
    """経費登録"""
    date: date
    category_id: str
    amount: int
    description: str = ""
    memo: Optional[str] = None


class IncomeCreate(BaseModel):
    """売上登録"""
    date: date
    amount: int
    description: str = ""
    client_name: Optional[str] = None
    memo: Optional[str] = None


class ExpenseResponse(BaseModel):
    """経費レスポンス"""
    id: str
    date: str
    category_id: str
    category_name: str
    amount: int
    description: str
    memo: Optional[str] = None
    is_expense: bool
    created_at: str


class IncomeResponse(BaseModel):
    """売上レスポンス"""
    id: str
    date: str
    amount: int
    description: str
    client_name: Optional[str] = None
    memo: Optional[str] = None
    created_at: str


class MonthlySummary(BaseModel):
    """月次サマリ"""
    year: int
    month: int
    total_income: int
    total_expense: int
    profit: int
    expense_count: int
    income_count: int


class DashboardSummary(BaseModel):
    """ダッシュボードサマリ"""
    this_month_income: int
    this_month_expense: int
    this_month_profit: int
    ytd_income: int
    ytd_expense: int
    ytd_profit: int
    recent_expenses: List[Dict[str, Any]]
    recent_income: List[Dict[str, Any]]
