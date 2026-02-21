"""
イベントストリーミングAPIエンドポイント
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user

from .cqrs import Command, Query, cqrs_bus
from .event_sourcing import DomainEvent, EventSourcingHandler, EventStore
from .kafka_client import KafkaClient
from .models import (CommandCreate, DomainEventCreate, EventConsume,
                     EventPublish, QueryCreate, TopicCreate)

router = APIRouter(prefix="/api/v1/events", tags=["イベントストリーミング"])

# Kafkaクライアントとイベントストアのインスタンス
kafka_client = KafkaClient()
event_store = EventStore(kafka_client)
event_sourcing_handler = EventSourcingHandler(event_store)

# CQRS と Kafka の連携（コマンド実行時に cqrs-commands トピックへイベント発行）
from .cqrs import set_cqrs_kafka_client

set_cqrs_kafka_client(kafka_client)


@router.get("/topics")
async def list_topics(current_user: Dict[str, Any] = Depends(get_current_active_user)):
    """トピック一覧を取得"""
    try:
        topics = kafka_client.list_topics()
        return {"topics": topics}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/topics", status_code=status.HTTP_201_CREATED)
async def create_topic(
    topic_data: TopicCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """トピックを作成"""
    try:
        created = kafka_client.create_topic(
            topic_data.name,
            num_partitions=topic_data.num_partitions,
            replication_factor=topic_data.replication_factor,
        )
        if not created:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Topic already exists"
            )
        return {"message": "Topic created successfully", "topic": topic_data.name}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/topics/{topic_name}")
async def get_topic_info(
    topic_name: str, current_user: Dict[str, Any] = Depends(get_current_active_user)
):
    """トピック情報を取得"""
    try:
        info = kafka_client.get_topic_info(topic_name)
        return info
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/publish")
async def publish_event(
    event_data: EventPublish,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """イベントを発行"""
    try:
        success = kafka_client.publish_event(
            topic=event_data.topic,
            event_type=event_data.event_type,
            data=event_data.data,
            key=event_data.key,
        )
        if success:
            return {
                "message": "Event published successfully",
                "topic": event_data.topic,
                "event_type": event_data.event_type,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to publish event",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/consume")
async def consume_events(
    topic: str,
    group_id: str,
    max_messages: int = 10,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """イベントを消費"""
    try:
        messages = kafka_client.consume_events(
            topic=topic, group_id=group_id, max_messages=max_messages
        )
        return {"messages": messages, "count": len(messages)}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# Event Sourcingエンドポイント
@router.post("/events", status_code=status.HTTP_201_CREATED)
async def create_domain_event(
    event_data: DomainEventCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ドメインイベントを作成"""
    try:
        # 集約の現在のバージョンを取得
        existing_events = event_store.get_events(
            aggregate_type=event_data.aggregate_type,
            aggregate_id=event_data.aggregate_id,
            max_events=1,
        )
        next_version = len(existing_events) + 1

        event = DomainEvent(
            event_id=str(uuid.uuid4()),
            aggregate_id=event_data.aggregate_id,
            aggregate_type=event_data.aggregate_type,
            event_type=event_data.event_type,
            event_data=event_data.event_data,
            timestamp=datetime.utcnow(),
            version=next_version,
            metadata=event_data.metadata,
        )

        success = event_store.append_event(event)
        if success:
            # イベントを適用して集約状態を更新
            aggregate = event_sourcing_handler.apply_event(event)
            return {
                "message": "Event created successfully",
                "event_id": event.event_id,
                "aggregate": aggregate,
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create event",
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/aggregates/{aggregate_type}/{aggregate_id}")
async def get_aggregate_state(
    aggregate_type: str,
    aggregate_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """集約状態を取得"""
    try:
        # イベント履歴から集約を再構築
        aggregate = event_sourcing_handler.rebuild_aggregate(
            aggregate_type=aggregate_type, aggregate_id=aggregate_id
        )

        if not aggregate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Aggregate not found"
            )

        return aggregate
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.get("/aggregates/{aggregate_type}/{aggregate_id}/events")
async def get_aggregate_events(
    aggregate_type: str,
    aggregate_id: str,
    max_events: int = 100,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """集約のイベント履歴を取得"""
    try:
        events = event_store.get_events(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            max_events=max_events,
        )
        return {
            "aggregate_type": aggregate_type,
            "aggregate_id": aggregate_id,
            "events": [event.dict() for event in events],
            "count": len(events),
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


# CQRSエンドポイント
@router.post("/commands")
async def execute_command(
    command_data: CommandCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """コマンドを実行（書き込み操作）"""
    try:
        command = Command(
            command_id=str(uuid.uuid4()),
            command_type=command_data.command_type,
            aggregate_id=command_data.aggregate_id,
            command_data=command_data.command_data,
            timestamp=datetime.utcnow(),
            user_id=current_user["username"],
        )

        result = await cqrs_bus.execute_command(command)
        return {"command_id": command.command_id, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/queries")
async def execute_query(
    query_data: QueryCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """クエリを実行（読み取り操作）"""
    try:
        query = Query(
            query_id=str(uuid.uuid4()),
            query_type=query_data.query_type,
            query_params=query_data.query_params,
            timestamp=datetime.utcnow(),
            user_id=current_user["username"],
        )

        result = await cqrs_bus.execute_query(query)
        return {"query_id": query.query_id, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
