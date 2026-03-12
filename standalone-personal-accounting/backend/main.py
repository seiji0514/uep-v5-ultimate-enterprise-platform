"""
個人会計API - スタンドアロン版
UEP v5.0 から独立。認証なし・単独動作。
"""
from datetime import date
from typing import Optional

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, Response, StreamingResponse
from pydantic import BaseModel

from expense_categories import ALL_CATEGORIES, get_expense_judgment, suggest_category
from invoice_pdf import REPORTLAB_AVAILABLE, generate_invoice_pdf
from receipt_ocr import extract_from_image
from store import (
    IS_PRACTICE,
    add_expense,
    add_income,
    delete_expense,
    delete_income,
    get_dashboard_summary,
    get_expenses,
    get_income,
    get_monthly_summary,
    get_receipt_path,
    save_receipt,
    update_expense,
)
from store import get_expenses as _get_expenses, get_income as _get_income, _load_data, _save_data
from store_ext import (
    FILES_DIR,
    add_client,
    add_contract,
    add_estimate,
    add_invoice,
    add_schedule,
    add_shared_file,
    add_task,
    add_work_hour,
    delete_client,
    delete_contract,
    delete_estimate,
    delete_invoice,
    delete_schedule,
    delete_shared_file,
    delete_task,
    delete_work_hour,
    get_clients,
    get_contracts,
    get_estimates,
    get_invoices,
    get_schedules,
    get_shared_files,
    get_tasks,
    get_work_hours,
    update_client,
    update_invoice_payment,
    update_task,
)
from contract_pdf import REPORTLAB_AVAILABLE as CONTRACT_PDF_AVAILABLE, generate_contract_pdf
from estimate_pdf import REPORTLAB_AVAILABLE as ESTIMATE_PDF_AVAILABLE, generate_estimate_pdf

app = FastAPI(title="個人会計 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExpenseCreate(BaseModel):
    date: date
    category_id: str
    amount: int
    description: str = ""
    memo: Optional[str] = None
    is_approved: bool = False
    approval_date: Optional[str] = None
    payment_method: Optional[str] = None


class ExpenseUpdate(BaseModel):
    is_approved: Optional[bool] = None
    approval_date: Optional[str] = None
    payment_method: Optional[str] = None


class IncomeCreate(BaseModel):
    date: date
    amount: int
    description: str = ""
    client_name: Optional[str] = None
    memo: Optional[str] = None


class TaskCreate(BaseModel):
    title: str
    description: str = ""
    client: str = ""
    due_date: str = ""
    status: str = "todo"


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    client: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None


class ScheduleCreate(BaseModel):
    title: str
    date: str
    start_time: str = ""
    end_time: str = ""
    memo: str = ""


class ContractCreate(BaseModel):
    client_name: str
    title: str
    amount: int
    start_date: str
    end_date: str
    description: str = ""


class EstimateCreate(BaseModel):
    client_name: str
    title: str
    amount: int
    valid_until: str = ""
    description: str = ""


class WorkHourCreate(BaseModel):
    date: str
    hours: float
    description: str = ""
    client: str = ""


class ClientCreate(BaseModel):
    name: str
    contact: str = ""
    address: str = ""
    memo: str = ""


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    memo: Optional[str] = None


class InvoiceRecordCreate(BaseModel):
    client_name: str
    amount: int
    description: str = "業務委託料"
    invoice_no: str = ""
    issue_date: str = ""


class InvoicePaymentUpdate(BaseModel):
    payment_status: str
    paid_date: str = ""


class InvoiceCreate(BaseModel):
    client_name: str
    client_address: str = ""
    client_contact: str = ""
    amount: int
    description: str = "業務委託料"
    invoice_no: str = "OGT-2026-001"
    bank_name: str = "〇〇銀行"
    bank_branch: str = "〇〇支店"
    bank_account: str = "〇〇〇〇〇〇〇"
    bank_holder: str = "オガワ セイジ"


@app.get("/")
def root():
    return {
        "message": "個人会計 API",
        "version": "1.0.0",
        "mode": "practice" if IS_PRACTICE else "production",
        "docs": "/docs",
    }


@app.get("/api/v1/categories")
def list_categories():
    return {
        "categories": [
            {"id": k, "name": v["name"], "is_expense": v["is_expense"], "note": v.get("note", "")}
            for k, v in ALL_CATEGORIES.items()
        ]
    }


@app.get("/api/v1/categories/suggest")
def suggest_categories(q: str = Query(..., min_length=1)):
    return {"suggestions": suggest_category(q)}


@app.get("/api/v1/dashboard")
def get_dashboard():
    data = get_dashboard_summary()
    data["mode"] = "practice" if IS_PRACTICE else "production"
    return data


@app.get("/api/v1/expenses")
def list_expenses(year: Optional[int] = None, month: Optional[int] = None):
    items = get_expenses(year, month)
    return {"items": items, "total": len(items)}


@app.post("/api/v1/expenses")
def create_expense(body: ExpenseCreate):
    return add_expense(
        body.date.isoformat(),
        body.category_id,
        body.amount,
        body.description,
        body.memo,
        is_approved=body.is_approved,
        approval_date=body.approval_date,
        payment_method=body.payment_method,
    )


@app.post("/api/v1/expenses/with-receipt")
async def create_expense_with_receipt(
    date: str = Form(...),
    category_id: str = Form(...),
    amount: int = Form(...),
    description: str = Form(""),
    memo: str = Form(""),
    is_approved: str = Form(""),
    approval_date: str = Form(""),
    payment_method: str = Form(""),
    receipt: UploadFile = File(None),
):
    """経費を登録し、領収書画像を紐付けて保存"""
    item = add_expense(
        date,
        category_id,
        amount,
        description,
        memo=memo or None,
        is_approved=is_approved.lower() in ("true", "on", "1") if is_approved else False,
        approval_date=approval_date or None,
        payment_method=payment_method or None,
    )
    if receipt and receipt.filename:
        data = await receipt.read()
        if len(data) > 0 and len(data) < 10 * 1024 * 1024:
            ext = "png" if (receipt.content_type or "").startswith("image/png") else "jpg"
            if save_receipt(item["id"], data, ext):
                item["receipt_filename"] = f"{item['id']}.{ext}"
    return item


@app.get("/api/v1/expenses/{expense_id}/receipt")
def get_expense_receipt(expense_id: str):
    """領収書画像を取得（ダウンロード用）"""
    path = get_receipt_path(expense_id)
    if not path:
        raise HTTPException(status_code=404, detail="領収書がありません")
    media = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return FileResponse(path, media_type=media)


@app.put("/api/v1/expenses/{expense_id}/receipt")
async def attach_receipt_to_expense(expense_id: str, receipt: UploadFile = File(...)):
    """既存の経費に領収書を紐付け"""
    expenses = get_expenses()
    if not any(e["id"] == expense_id for e in expenses):
        raise HTTPException(status_code=404, detail="Expense not found")
    img = await receipt.read()
    if len(img) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="ファイルサイズは10MB以下にしてください")
    ext = "png" if (receipt.content_type or "").startswith("image/png") else "jpg"
    if save_receipt(expense_id, img, ext):
        return {"message": "領収書を紐付けました"}
    raise HTTPException(status_code=500, detail="保存に失敗しました")


@app.patch("/api/v1/expenses/{expense_id}")
def patch_expense(expense_id: str, body: ExpenseUpdate):
    """経費の電子決裁・支払い方法を更新"""
    item = update_expense(
        expense_id,
        is_approved=body.is_approved,
        approval_date=body.approval_date,
        payment_method=body.payment_method,
    )
    if not item:
        raise HTTPException(status_code=404, detail="Expense not found")
    return item


@app.delete("/api/v1/expenses/{expense_id}")
def remove_expense(expense_id: str):
    if not delete_expense(expense_id):
        raise HTTPException(status_code=404, detail="Expense not found")
    return {"message": "deleted"}


@app.get("/api/v1/income")
def list_income(year: Optional[int] = None, month: Optional[int] = None):
    items = get_income(year, month)
    return {"items": items, "total": len(items)}


@app.post("/api/v1/income")
def create_income(body: IncomeCreate):
    return add_income(
        body.date.isoformat(),
        body.amount,
        body.description,
        body.client_name,
        body.memo,
    )


@app.delete("/api/v1/income/{income_id}")
def remove_income(income_id: str):
    if not delete_income(income_id):
        raise HTTPException(status_code=404, detail="Income not found")
    return {"message": "deleted"}


@app.get("/api/v1/summary/monthly")
def get_monthly(year: int = Query(...), month: int = Query(..., ge=1, le=12)):
    return get_monthly_summary(year, month)


# --- 領収書OCR ---
@app.post("/api/v1/receipts/ocr")
async def receipt_ocr(file: UploadFile = File(...)):
    """領収書画像をアップロードし、日付・金額・店名を抽出"""
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="画像ファイルをアップロードしてください")
    data = await file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="ファイルサイズは10MB以下にしてください")
    return extract_from_image(data)


# --- 確定申告書（収支内訳書風HTML） ---
@app.get("/api/v1/tax-declaration/{year}", response_class=HTMLResponse)
def tax_declaration(
    year: int,
    name: str = Query("小川 清志", description="氏名"),
    address: str = Query("", description="住所"),
):
    from tax_declaration import generate_tax_declaration_html

    html = generate_tax_declaration_html(year, name, address)
    return HTMLResponse(content=html)


# --- 請求書PDF ---
@app.post("/api/v1/invoice/pdf")
def invoice_pdf(body: InvoiceCreate):
    """請求書PDFを生成して返す"""
    if not REPORTLAB_AVAILABLE:
        raise HTTPException(status_code=503, detail="reportlab がインストールされていません")
    pdf_bytes = generate_invoice_pdf(
        body.client_name,
        body.amount,
        client_address=body.client_address,
        client_contact=body.client_contact,
        description=body.description,
        invoice_no=body.invoice_no,
        bank_name=body.bank_name,
        bank_branch=body.bank_branch,
        bank_account=body.bank_account,
        bank_holder=body.bank_holder,
    )
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="PDF生成に失敗しました")
    return Response(content=pdf_bytes, media_type="application/pdf")


# --- Phase 1: タスク管理 ---
@app.get("/api/v1/tasks")
def list_tasks(status: Optional[str] = None):
    return {"items": get_tasks(status), "total": len(get_tasks(status))}


@app.post("/api/v1/tasks")
def create_task(body: TaskCreate):
    return add_task(body.title, body.description, body.client, body.due_date, body.status)


@app.patch("/api/v1/tasks/{task_id}")
def patch_task(task_id: str, body: TaskUpdate):
    kwargs = {k: v for k, v in body.model_dump().items() if v is not None}
    item = update_task(task_id, **kwargs)
    if not item:
        raise HTTPException(status_code=404, detail="Task not found")
    return item


@app.delete("/api/v1/tasks/{task_id}")
def remove_task(task_id: str):
    if not delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "deleted"}


# --- Phase 2: スケジュール管理 ---
@app.get("/api/v1/schedules")
def list_schedules(year: Optional[int] = None, month: Optional[int] = None):
    return {"items": get_schedules(year, month), "total": len(get_schedules(year, month))}


@app.post("/api/v1/schedules")
def create_schedule(body: ScheduleCreate):
    return add_schedule(body.title, body.date, body.start_time, body.end_time, body.memo)


@app.delete("/api/v1/schedules/{schedule_id}")
def remove_schedule(schedule_id: str):
    if not delete_schedule(schedule_id):
        raise HTTPException(status_code=404, detail="Schedule not found")
    return {"message": "deleted"}


# --- Phase 3: 契約書 ---
@app.get("/api/v1/contracts")
def list_contracts():
    return {"items": get_contracts(), "total": len(get_contracts())}


@app.post("/api/v1/contracts")
def create_contract(body: ContractCreate):
    return add_contract(body.client_name, body.title, body.amount, body.start_date, body.end_date, body.description)


@app.get("/api/v1/contracts/{contract_id}/pdf")
def contract_pdf(contract_id: str):
    contracts = get_contracts()
    c = next((x for x in contracts if x["id"] == contract_id), None)
    if not c:
        raise HTTPException(status_code=404, detail="Contract not found")
    if not CONTRACT_PDF_AVAILABLE:
        raise HTTPException(status_code=503, detail="reportlab がインストールされていません")
    pdf_bytes = generate_contract_pdf(
        c["client_name"], c["title"], c["amount"], c["start_date"], c["end_date"], c.get("description", "")
    )
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="PDF生成に失敗しました")
    return Response(content=pdf_bytes, media_type="application/pdf")


@app.delete("/api/v1/contracts/{contract_id}")
def remove_contract(contract_id: str):
    if not delete_contract(contract_id):
        raise HTTPException(status_code=404, detail="Contract not found")
    return {"message": "deleted"}


# --- Phase 4: ファイル共有 ---
@app.get("/api/v1/files")
def list_files(category: Optional[str] = None):
    return {"items": get_shared_files(category), "total": len(get_shared_files(category))}


@app.post("/api/v1/files")
async def upload_file(
    file: UploadFile = File(...),
    category: str = Form("その他"),
    description: str = Form(""),
):
    import uuid
    FILES_DIR.mkdir(parents=True, exist_ok=True)
    data = await file.read()
    if len(data) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="ファイルサイズは10MB以下にしてください")
    fid = str(uuid.uuid4())
    (FILES_DIR / fid).write_bytes(data)
    filename = file.filename or "file"
    return add_shared_file(filename, category, description, fid)


@app.get("/api/v1/files/{file_id}/download")
def download_file(file_id: str):
    """file_id はレコードID。実ファイルは file_id フィールドで参照"""
    items = get_shared_files()
    rec = next((f for f in items if f["id"] == file_id), None)
    if not rec:
        raise HTTPException(status_code=404, detail="File not found")
    path = FILES_DIR / rec["file_id"]
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path, filename=rec["filename"])


@app.delete("/api/v1/files/{file_id}")
def remove_file(file_id: str):
    if not delete_shared_file(file_id):
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "deleted"}


# --- 見積書 ---
@app.get("/api/v1/estimates")
def list_estimates():
    return {"items": get_estimates(), "total": len(get_estimates())}


@app.post("/api/v1/estimates")
def create_estimate(body: EstimateCreate):
    return add_estimate(body.client_name, body.title, body.amount, body.valid_until, body.description)


@app.get("/api/v1/estimates/{estimate_id}/pdf")
def estimate_pdf(estimate_id: str):
    estimates = get_estimates()
    e = next((x for x in estimates if x["id"] == estimate_id), None)
    if not e:
        raise HTTPException(status_code=404, detail="Estimate not found")
    if not ESTIMATE_PDF_AVAILABLE:
        raise HTTPException(status_code=503, detail="reportlab がインストールされていません")
    pdf_bytes = generate_estimate_pdf(e["client_name"], e["title"], e["amount"], e.get("valid_until", ""), e.get("description", ""))
    if not pdf_bytes:
        raise HTTPException(status_code=500, detail="PDF生成に失敗しました")
    return Response(content=pdf_bytes, media_type="application/pdf")


@app.delete("/api/v1/estimates/{estimate_id}")
def remove_estimate(estimate_id: str):
    if not delete_estimate(estimate_id):
        raise HTTPException(status_code=404, detail="Estimate not found")
    return {"message": "deleted"}


# --- 稼働時間管理 ---
@app.get("/api/v1/work-hours")
def list_work_hours(year: Optional[int] = None, month: Optional[int] = None):
    items = get_work_hours(year, month)
    total = sum(w.get("hours", 0) for w in items)
    return {"items": items, "total": len(items), "total_hours": total}


@app.post("/api/v1/work-hours")
def create_work_hour(body: WorkHourCreate):
    return add_work_hour(body.date, body.hours, body.description, body.client)


@app.delete("/api/v1/work-hours/{wh_id}")
def remove_work_hour(wh_id: str):
    if not delete_work_hour(wh_id):
        raise HTTPException(status_code=404, detail="Work hour not found")
    return {"message": "deleted"}


# --- クライアント管理 ---
@app.get("/api/v1/clients")
def list_clients():
    return {"items": get_clients(), "total": len(get_clients())}


@app.post("/api/v1/clients")
def create_client(body: ClientCreate):
    return add_client(body.name, body.contact, body.address, body.memo)


@app.patch("/api/v1/clients/{client_id}")
def patch_client(client_id: str, body: ClientUpdate):
    kwargs = {k: v for k, v in body.model_dump().items() if v is not None}
    item = update_client(client_id, **kwargs)
    if not item:
        raise HTTPException(status_code=404, detail="Client not found")
    return item


@app.delete("/api/v1/clients/{client_id}")
def remove_client(client_id: str):
    if not delete_client(client_id):
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "deleted"}


# --- 請求・支払い状況 ---
@app.get("/api/v1/invoices")
def list_invoices(status: Optional[str] = None):
    return {"items": get_invoices(status), "total": len(get_invoices(status))}


@app.post("/api/v1/invoices")
def create_invoice_record(body: InvoiceRecordCreate):
    return add_invoice(body.client_name, body.amount, body.description, body.invoice_no, body.issue_date)


@app.patch("/api/v1/invoices/{invoice_id}/payment")
def patch_invoice_payment(invoice_id: str, body: InvoicePaymentUpdate):
    item = update_invoice_payment(invoice_id, body.payment_status, body.paid_date)
    if not item:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return item


@app.delete("/api/v1/invoices/{invoice_id}")
def remove_invoice(invoice_id: str):
    if not delete_invoice(invoice_id):
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {"message": "deleted"}


# --- CSV エクスポート ---
@app.get("/api/v1/export/csv")
def export_csv(data_type: str = Query("expenses", regex="^(expenses|income|tasks|work_hours|invoices)$")):
    import csv
    from io import StringIO
    if data_type == "expenses":
        items = _get_expenses()
        fieldnames = ["date", "category_name", "description", "amount", "payment_method", "is_approved"]
        rows = [{k: e.get(k, "") for k in fieldnames} for e in items]
    elif data_type == "income":
        items = _get_income()
        fieldnames = ["date", "description", "client_name", "amount"]
        rows = [{k: i.get(k, "") for k in fieldnames} for i in items]
    elif data_type == "tasks":
        items = get_tasks()
        fieldnames = ["title", "client", "due_date", "status", "description"]
        rows = [{k: t.get(k, "") for k in fieldnames} for t in items]
    elif data_type == "work_hours":
        items = get_work_hours()
        fieldnames = ["date", "hours", "description", "client"]
        rows = [{k: w.get(k, "") for k in fieldnames} for w in items]
    else:
        items = get_invoices()
        fieldnames = ["client_name", "amount", "issue_date", "payment_status", "paid_date"]
        rows = [{k: inv.get(k, "") for k in fieldnames} for inv in items]
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": f"attachment; filename={data_type}.csv"})


# --- 月次レポート ---
@app.get("/api/v1/reports/monthly")
def monthly_report(year: int = Query(...), month: int = Query(..., ge=1, le=12)):
    expenses = _get_expenses(year, month)
    income = _get_income(year, month)
    by_cat = {}
    for e in expenses:
        c = e.get("category_name", "その他")
        by_cat[c] = by_cat.get(c, 0) + e.get("amount", 0)
    work_hours = get_work_hours(year, month)
    total_hours = sum(w.get("hours", 0) for w in work_hours)
    return {
        "year": year,
        "month": month,
        "total_income": sum(i["amount"] for i in income),
        "total_expense": sum(e["amount"] for e in expenses),
        "profit": sum(i["amount"] for i in income) - sum(e["amount"] for e in expenses),
        "by_category": by_cat,
        "work_hours": total_hours,
        "income_count": len(income),
        "expense_count": len(expenses),
    }


# --- データバックアップ ---
@app.get("/api/v1/backup/export")
def backup_export():
    data = _load_data()
    import json
    return Response(
        content=json.dumps(data, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=backup.json"},
    )


@app.post("/api/v1/backup/import")
async def backup_import(file: UploadFile = File(...)):
    data = await file.read()
    try:
        import json
        parsed = json.loads(data.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise ValueError("Invalid format")
        _save_data(parsed)
        return {"message": "インポートしました"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"インポートエラー: {str(e)}")


if __name__ == "__main__":
    import os
    import uvicorn
    port = int(os.environ.get("PERSONAL_ACCOUNTING_PORT", "5000"))
    mode = os.environ.get("PERSONAL_ACCOUNTING_MODE", "production")
    print(f"Mode: {mode} | Port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
