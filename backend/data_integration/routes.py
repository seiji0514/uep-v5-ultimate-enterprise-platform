"""
産業統合プラットフォーム - 実データ連携 API（Phase 2）
CSV取り込み・DB保存・レポート出力
"""
from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/data-integration", tags=["実データ連携"])

# インメモリストア（本番ではDBに置き換え）
_csv_store: List[Dict[str, Any]] = []


class CsvImportRequest(BaseModel):
    rows: List[List[str]]
    domain: str = "general"


class CsvImportResponse(BaseModel):
    saved: int
    domain: str


@router.post("/csv", response_model=CsvImportResponse)
async def import_csv(data: CsvImportRequest):
    """CSVデータを保存（Phase 2: DB連携の基盤）"""
    global _csv_store
    if not data.rows:
        raise HTTPException(status_code=400, detail="rows が空です")
    headers = data.rows[0] if data.rows else []
    for row in data.rows[1:]:
        obj = {"domain": data.domain, "_headers": headers}
        for i, h in enumerate(headers):
            obj[h] = row[i] if i < len(row) else ""
        _csv_store.append(obj)
    return CsvImportResponse(saved=len(data.rows) - 1, domain=data.domain)


@router.get("/csv")
async def get_stored_csv(domain: str | None = None):
    """保存済みCSVデータを取得"""
    items = _csv_store
    if domain:
        items = [x for x in items if x.get("domain") == domain]
    return {"items": items, "total": len(items)}
