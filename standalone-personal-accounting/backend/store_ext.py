"""
拡張ストア: タスク・スケジュール・契約書・ファイル共有
"""
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from store import DATA_DIR, DATA_FILE, IS_PRACTICE, _ensure_data_dir, _load_data, _save_data

FILES_DIR = DATA_DIR / ("shared_files_practice" if IS_PRACTICE else "shared_files")


def _ensure_files_dir():
    FILES_DIR.mkdir(parents=True, exist_ok=True)


def _ensure_ext_keys(data: dict) -> dict:
    for key in ["tasks", "schedules", "contracts", "shared_files", "estimates", "work_hours", "clients", "invoices"]:
        if key not in data:
            data[key] = []
    return data


# --- Phase 1: タスク管理 ---
def add_task(title: str, description: str = "", client: str = "", due_date: str = "", status: str = "todo") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "title": title,
        "description": description or "",
        "client": client or "",
        "due_date": due_date or "",
        "status": status,
        "created_at": datetime.utcnow().isoformat(),
    }
    data["tasks"].append(item)
    _save_data(data)
    return item


def get_tasks(status: Optional[str] = None) -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    items = data["tasks"]
    if status:
        items = [t for t in items if t.get("status") == status]
    return sorted(items, key=lambda x: (x.get("due_date") or "9999"), reverse=True)


def update_task(task_id: str, **kwargs) -> Optional[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    for t in data["tasks"]:
        if t["id"] == task_id:
            for k, v in kwargs.items():
                if k in t and v is not None:
                    t[k] = v
            _save_data(data)
            return t
    return None


def delete_task(task_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["tasks"])
    data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
    if len(data["tasks"]) < orig:
        _save_data(data)
        return True
    return False


# --- Phase 2: スケジュール管理 ---
def add_schedule(title: str, date_str: str, start_time: str = "", end_time: str = "", memo: str = "") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "title": title,
        "date": date_str,
        "start_time": start_time or "",
        "end_time": end_time or "",
        "memo": memo or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["schedules"].append(item)
    _save_data(data)
    return item


def get_schedules(year: Optional[int] = None, month: Optional[int] = None) -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    items = data["schedules"]
    if year:
        items = [s for s in items if s.get("date", "").startswith(f"{year}-")]
    if month:
        items = [s for s in items if s.get("date", "")[5:7] == f"{month:02d}"]
    return sorted(items, key=lambda x: (x.get("date", ""), x.get("start_time", "")))


def delete_schedule(schedule_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["schedules"])
    data["schedules"] = [s for s in data["schedules"] if s["id"] != schedule_id]
    if len(data["schedules"]) < orig:
        _save_data(data)
        return True
    return False


# --- Phase 3: 契約書 ---
def add_contract(client_name: str, title: str, amount: int, start_date: str, end_date: str, description: str = "") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "client_name": client_name,
        "title": title,
        "amount": amount,
        "start_date": start_date,
        "end_date": end_date,
        "description": description or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["contracts"].append(item)
    _save_data(data)
    return item


def get_contracts() -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    return sorted(data["contracts"], key=lambda x: x.get("created_at", ""), reverse=True)


def delete_contract(contract_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["contracts"])
    data["contracts"] = [c for c in data["contracts"] if c["id"] != contract_id]
    if len(data["contracts"]) < orig:
        _save_data(data)
        return True
    return False


# --- Phase 4: ファイル共有 ---
def add_shared_file(filename: str, category: str, description: str, file_id: str) -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "file_id": file_id,
        "filename": filename,
        "category": category or "その他",
        "description": description or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["shared_files"].append(item)
    _save_data(data)
    return item


def get_shared_files(category: Optional[str] = None) -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    items = data["shared_files"]
    if category:
        items = [f for f in items if f.get("category") == category]
    return sorted(items, key=lambda x: x.get("created_at", ""), reverse=True)


# --- 見積書 ---
def add_estimate(client_name: str, title: str, amount: int, valid_until: str = "", description: str = "") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "client_name": client_name,
        "title": title,
        "amount": amount,
        "valid_until": valid_until or "",
        "description": description or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["estimates"].append(item)
    _save_data(data)
    return item


def get_estimates() -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    return sorted(data["estimates"], key=lambda x: x.get("created_at", ""), reverse=True)


def delete_estimate(estimate_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["estimates"])
    data["estimates"] = [e for e in data["estimates"] if e["id"] != estimate_id]
    if len(data["estimates"]) < orig:
        _save_data(data)
        return True
    return False


# --- 稼働時間管理 ---
def add_work_hour(date_str: str, hours: float, description: str = "", client: str = "", task_id: str = "") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "date": date_str,
        "hours": hours,
        "description": description or "",
        "client": client or "",
        "task_id": task_id or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["work_hours"].append(item)
    _save_data(data)
    return item


def get_work_hours(year: Optional[int] = None, month: Optional[int] = None) -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    items = data["work_hours"]
    if year:
        items = [w for w in items if w.get("date", "").startswith(f"{year}-")]
    if month:
        items = [w for w in items if w.get("date", "")[5:7] == f"{month:02d}"]
    return sorted(items, key=lambda x: (x.get("date", ""),), reverse=True)


def delete_work_hour(wh_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["work_hours"])
    data["work_hours"] = [w for w in data["work_hours"] if w["id"] != wh_id]
    if len(data["work_hours"]) < orig:
        _save_data(data)
        return True
    return False


# --- クライアント管理 ---
def add_client(name: str, contact: str = "", address: str = "", memo: str = "") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "name": name,
        "contact": contact or "",
        "address": address or "",
        "memo": memo or "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["clients"].append(item)
    _save_data(data)
    return item


def get_clients() -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    return sorted(data["clients"], key=lambda x: x.get("name", ""))


def update_client(client_id: str, **kwargs) -> Optional[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    for c in data["clients"]:
        if c["id"] == client_id:
            for k, v in kwargs.items():
                if k in c and v is not None:
                    c[k] = v
            _save_data(data)
            return c
    return None


def delete_client(client_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["clients"])
    data["clients"] = [c for c in data["clients"] if c["id"] != client_id]
    if len(data["clients"]) < orig:
        _save_data(data)
        return True
    return False


# --- 請求・支払い状況 ---
def add_invoice(client_name: str, amount: int, description: str = "", invoice_no: str = "", issue_date: str = "") -> dict:
    data = _load_data()
    data = _ensure_ext_keys(data)
    item = {
        "id": str(uuid.uuid4()),
        "client_name": client_name,
        "amount": amount,
        "description": description or "業務委託料",
        "invoice_no": invoice_no or "",
        "issue_date": issue_date or "",
        "payment_status": "unpaid",
        "paid_date": "",
        "created_at": datetime.utcnow().isoformat(),
    }
    data["invoices"].append(item)
    _save_data(data)
    return item


def get_invoices(status: Optional[str] = None) -> List[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    items = data["invoices"]
    if status:
        items = [i for i in items if i.get("payment_status") == status]
    return sorted(items, key=lambda x: x.get("issue_date", "") or x.get("created_at", ""), reverse=True)


def update_invoice_payment(invoice_id: str, status: str, paid_date: str = "") -> Optional[dict]:
    data = _load_data()
    data = _ensure_ext_keys(data)
    for i in data["invoices"]:
        if i["id"] == invoice_id:
            i["payment_status"] = status
            i["paid_date"] = paid_date or ""
            _save_data(data)
            return i
    return None


def delete_invoice(invoice_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    orig = len(data["invoices"])
    data["invoices"] = [i for i in data["invoices"] if i["id"] != invoice_id]
    if len(data["invoices"]) < orig:
        _save_data(data)
        return True
    return False


def delete_shared_file(record_id: str) -> bool:
    data = _load_data()
    data = _ensure_ext_keys(data)
    fid = None
    for f in data["shared_files"]:
        if f["id"] == record_id:
            fid = f.get("file_id")
            break
    orig = len(data["shared_files"])
    data["shared_files"] = [f for f in data["shared_files"] if f["id"] != record_id]
    if len(data["shared_files"]) < orig:
        _save_data(data)
        if fid:
            try:
                (FILES_DIR / fid).unlink(missing_ok=True)
            except Exception:
                pass
        return True
    return False
