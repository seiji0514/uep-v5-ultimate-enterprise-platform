"""
統合ビジネスプラットフォーム - イベント発行
実用的最高難易度: イベント駆動設計・Kafka統合
"""
from typing import Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

# オプショナルKafka発行（Kafkaが利用可能な場合のみ）
_kafka_client = None


def _get_kafka_client():
    """Kafka Clientを取得（利用可能な場合）"""
    global _kafka_client
    if _kafka_client is not None:
        return _kafka_client
    try:
        from event_streaming.kafka_client import KafkaClient, KAFKA_AVAILABLE
        if KAFKA_AVAILABLE:
            _kafka_client = KafkaClient()
            return _kafka_client
    except Exception as e:
        logger.debug(f"Kafka not available for unified_business_platform: {e}")
    return None


def publish_event(
    topic: str,
    event_type: str,
    payload: Dict[str, Any],
    key: Optional[str] = None,
) -> bool:
    """
    イベントをKafkaに発行（Kafkaが利用可能な場合）
    実用的最高難易度: イベント駆動設計
    """
    client = _get_kafka_client()
    if client is None:
        return False
    try:
        return client.publish_event(
            topic=topic,
            event_type=event_type,
            data=payload,
            key=key,
        )
    except Exception as e:
        logger.warning(f"Failed to publish event to Kafka: {e}")
        return False


def publish_workflow_event(event_type: str, workflow_id: str, data: Dict[str, Any]) -> bool:
    """ワークフローイベントを発行"""
    return publish_event(
        topic="unified-business-workflow",
        event_type=event_type,
        payload={"workflow_id": workflow_id, **data},
        key=workflow_id,
    )


def publish_approval_event(event_type: str, request_id: str, data: Dict[str, Any]) -> bool:
    """承認イベントを発行"""
    return publish_event(
        topic="unified-business-approval",
        event_type=event_type,
        payload={"request_id": request_id, **data},
        key=request_id,
    )


def publish_ticket_event(event_type: str, ticket_id: str, data: Dict[str, Any]) -> bool:
    """チケットイベントを発行"""
    return publish_event(
        topic="unified-business-tickets",
        event_type=event_type,
        payload={"ticket_id": ticket_id, **data},
        key=ticket_id,
    )
