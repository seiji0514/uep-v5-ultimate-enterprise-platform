"""
データカタログモジュール
データのメタデータ管理
"""
from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from typing import List as ListType


class DataCatalogEntry(BaseModel):
    """データカタログエントリ"""
    id: str
    name: str
    description: Optional[str] = None
    bucket_name: str
    object_name: str
    data_type: str  # raw, processed, model, dataset, backup
    format: str  # parquet, csv, json, pickle, etc.
    schema: Optional[Dict[str, Any]] = None
    tags: List[str] = []
    owner: str
    created_at: datetime
    updated_at: datetime
    size: int
    version: int = 1
    metadata: Optional[Dict[str, Any]] = None


class DataCatalog:
    """データカタログクラス"""

    def __init__(self):
        """データカタログを初期化"""
        # 簡易的なインメモリストレージ（実際の実装ではデータベースを使用）
        self._catalog: Dict[str, DataCatalogEntry] = {}

    def register(
        self,
        name: str,
        bucket_name: str,
        object_name: str,
        data_type: str,
        format: str,
        owner: str,
        description: Optional[str] = None,
        schema: Optional[Dict[str, Any]] = None,
        tags: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        size: int = 0
    ) -> DataCatalogEntry:
        """データカタログに登録"""
        catalog_id = f"{bucket_name}/{object_name}"
        now = datetime.utcnow()

        entry = DataCatalogEntry(
            id=catalog_id,
            name=name,
            description=description,
            bucket_name=bucket_name,
            object_name=object_name,
            data_type=data_type,
            format=format,
            schema=schema,
            tags=tags or [],
            owner=owner,
            created_at=now,
            updated_at=now,
            size=size,
            metadata=metadata
        )

        self._catalog[catalog_id] = entry
        return entry

    def get(self, catalog_id: str) -> Optional[DataCatalogEntry]:
        """カタログエントリを取得"""
        return self._catalog.get(catalog_id)

    def list(
        self,
        data_type: Optional[str] = None,
        owner: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> List[DataCatalogEntry]:
        """カタログエントリ一覧を取得"""
        entries = list(self._catalog.values())

        if data_type:
            entries = [e for e in entries if e.data_type == data_type]

        if owner:
            entries = [e for e in entries if e.owner == owner]

        if tags:
            entries = [e for e in entries if any(tag in e.tags for tag in tags)]

        return entries

    def update(
        self,
        catalog_id: str,
        **kwargs
    ) -> Optional[DataCatalogEntry]:
        """カタログエントリを更新"""
        entry = self._catalog.get(catalog_id)
        if not entry:
            return None

        # 更新可能なフィールドを更新
        update_fields = {
            "name", "description", "schema", "tags", "metadata"
        }

        for key, value in kwargs.items():
            if key in update_fields:
                setattr(entry, key, value)

        entry.updated_at = datetime.utcnow()
        entry.version += 1

        return entry

    def delete(self, catalog_id: str) -> bool:
        """カタログエントリを削除"""
        if catalog_id in self._catalog:
            del self._catalog[catalog_id]
            return True
        return False

    def search(self, query: str) -> List[DataCatalogEntry]:
        """カタログを検索"""
        query_lower = query.lower()
        results = []

        for entry in self._catalog.values():
            if (
                query_lower in entry.name.lower() or
                (entry.description and query_lower in entry.description.lower()) or
                any(query_lower in tag.lower() for tag in entry.tags)
            ):
                results.append(entry)

        return results


# グローバルインスタンス
catalog = DataCatalog()
