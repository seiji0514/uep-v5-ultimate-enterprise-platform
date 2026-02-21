"""
イベントストリーミング関連のデータモデル
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class TopicCreate(BaseModel):
    """トピック作成モデル"""
    name: str
    num_partitions: int = 1
    replication_factor: int = 1


class EventPublish(BaseModel):
    """イベント発行モデル"""
    topic: str
    event_type: str
    data: Dict[str, Any]
    key: Optional[str] = None


class EventConsume(BaseModel):
    """イベント消費モデル"""
    topic: str
    group_id: str
    max_messages: int = 10
    auto_offset_reset: str = "earliest"


class DomainEventCreate(BaseModel):
    """ドメインイベント作成モデル"""
    aggregate_id: str
    aggregate_type: str
    event_type: str
    event_data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class CommandCreate(BaseModel):
    """コマンド作成モデル"""
    command_type: str
    aggregate_id: Optional[str] = None
    command_data: Dict[str, Any]


class QueryCreate(BaseModel):
    """クエリ作成モデル"""
    query_type: str
    query_params: Dict[str, Any]
