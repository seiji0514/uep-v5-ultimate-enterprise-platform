"""
Kafkaプロデューサー設定
"""

from kafka import KafkaProducer
from kafka.errors import KafkaError
import json
from app.core.config import settings
from loguru import logger

# Kafkaプロデューサーの作成
kafka_producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: k.encode('utf-8') if k else None
)


def send_message(topic: str, message: dict, key: str = None):
    """メッセージの送信"""
    try:
        future = kafka_producer.send(topic, value=message, key=key)
        record_metadata = future.get(timeout=10)
        logger.info(f"メッセージ送信成功: topic={topic}, partition={record_metadata.partition}, offset={record_metadata.offset}")
        return True
    except KafkaError as e:
        logger.error(f"メッセージ送信エラー: {e}")
        return False

