"""
個人会計データストア（JSONファイル永続化）
"""
import json
import os
import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .expense_categories import ALL_CATEGORIES, get_expense_judgment

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
DATA_FILE = DATA_DIR / "personal_accounting.json"


def _ensure_data_dir():
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_data() -> dict:
    _ensure_data_dir()
    if not DATA_FILE.exists():
        return {"expenses": [], "income": []}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"expenses": [], "income": []}


def _save_data(data: dict):
    _ensure_data_dir()
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def add_expense(date_str: str, category_id: str, amount: int, description: str = "", memo: Optional[str] = None) -> dict:
    data = _load_data()
    cat = ALL_CATEGORIES.get(category_id, {})
    judgment = get_expense_judgment(category_id)
    item = {
        "id": str(uuid.uuid4()),
        "date": date_str,
        "category_id": category_id,
        "category_name": cat.get("name", category_id),
        "amount": amount,
        "description": description or "",
        "memo": memo,
        "is_expense": judgment["is_expense"],
        "created_at": datetime.utcnow().isoformat(),
    }
    data["expenses"].append(item)
    _save_data(data)
    return item


def add_income(date_str: str, amount: int, description: str = "", client_name: Optional[str] = None, memo: Optional[str] = None) -> dict:
    data = _load_data()
    item = {
        "id": str(uuid.uuid4()),
        "date": date_str,
        "amount": amount,
        "description": description or "",
        "client_name": client_name,
        "memo": memo,
        "created_at": datetime.utcnow().isoformat(),
    }
    data["income"].append(item)
    _save_data(data)
    return item


def get_expenses(year: Optional[int] = None, month: Optional[int] = None) -> List[dict]:
    data = _load_data()
    items = data.get("expenses", [])
    if year is not None:
        items = [e for e in items if e["date"].startswith(f"{year}-")]
    if month is not None:
        items = [e for e in items if e["date"][5:7] == f"{month:02d}"]
    return sorted(items, key=lambda x: x["date"], reverse=True)


def get_income(year: Optional[int] = None, month: Optional[int] = None) -> List[dict]:
    data = _load_data()
    items = data.get("income", [])
    if year is not None:
        items = [e for e in items if e["date"].startswith(f"{year}-")]
    if month is not None:
        items = [e for e in items if e["date"][5:7] == f"{month:02d}"]
    return sorted(items, key=lambda x: x["date"], reverse=True)


def get_monthly_summary(year: int, month: int) -> dict:
    expenses = get_expenses(year, month)
    income = get_income(year, month)
    total_expense = sum(e["amount"] for e in expenses)
    total_income = sum(i["amount"] for i in income)
    return {
        "year": year,
        "month": month,
        "total_income": total_income,
        "total_expense": total_expense,
        "profit": total_income - total_expense,
        "expense_count": len(expenses),
        "income_count": len(income),
    }


def get_dashboard_summary() -> dict:
    today = date.today()
    this_month = get_monthly_summary(today.year, today.month)
    ytd_income = sum(i["amount"] for i in get_income() if i["date"].startswith(str(today.year)))
    ytd_expense = sum(e["amount"] for e in get_expenses() if e["date"].startswith(str(today.year)))
    return {
        "this_month_income": this_month["total_income"],
        "this_month_expense": this_month["total_expense"],
        "this_month_profit": this_month["profit"],
        "ytd_income": ytd_income,
        "ytd_expense": ytd_expense,
        "ytd_profit": ytd_income - ytd_expense,
        "recent_expenses": get_expenses()[:10],
        "recent_income": get_income()[:10],
    }


def delete_expense(expense_id: str) -> bool:
    data = _load_data()
    orig = len(data["expenses"])
    data["expenses"] = [e for e in data["expenses"] if e["id"] != expense_id]
    if len(data["expenses"]) < orig:
        _save_data(data)
        return True
    return False


def delete_income(income_id: str) -> bool:
    data = _load_data()
    orig = len(data["income"])
    data["income"] = [i for i in data["income"] if i["id"] != income_id]
    if len(data["income"]) < orig:
        _save_data(data)
        return True
    return False
