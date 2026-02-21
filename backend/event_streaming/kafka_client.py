"""
Kafkaクライアントモジュール
Apache Kafkaへの接続と操作を実装
"""
import logging
import warnings

# Kafka関連の警告を抑制
warnings.filterwarnings("ignore", message=".*kafka.*")
logging.getLogger("kafka").setLevel(logging.ERROR)

try:
    from kafka import KafkaAdminClient, KafkaConsumer, KafkaProducer
    from kafka.admin import NewTopic
    from kafka.errors import KafkaError

    KAFKA_AVAILABLE = True
except ImportError as e:
    # Kafkaが利用できない場合は警告を出さずに続行（ログレベルをERRORに設定済み）
    KAFKA_AVAILABLE = False
    KafkaProducer = None
    KafkaConsumer = None
    KafkaAdminClient = None
    NewTopic = None
    KafkaError = Exception

import json
import os
from datetime import datetime
from typing import Any, Dict, List, Optional


class KafkaClient:
    """Kafkaクライアントクラス"""

    def __init__(
        self, bootstrap_servers: Optional[str] = None, client_id: Optional[str] = None
    ):
        """
        Kafkaクライアントを初期化

        Args:
            bootstrap_servers: Kafkaブローカーのアドレス（デフォルト: 環境変数から取得）
            client_id: クライアントID
        """
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            "KAFKA_BOOTSTRAP_SERVERS", "kafka:9092"
        )
        self.client_id = client_id or "uep-v5-client"

        # ProducerとConsumerは必要に応じて作成
        self._producer: Optional[KafkaProducer] = None
        self._admin: Optional[KafkaAdminClient] = None

    def _get_producer(self) -> KafkaProducer:
        """Producerを取得（必要に応じて作成）"""
        if not KAFKA_AVAILABLE:
            raise RuntimeError(
                "Kafka is not available. Please install kafka-python and six packages."
            )
        if self._producer is None:
            self._producer = KafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps(v).encode("utf-8"),
                key_serializer=lambda k: k.encode("utf-8") if k else None,
                client_id=self.client_id,
            )
        return self._producer

    def _get_admin(self) -> KafkaAdminClient:
        """AdminClientを取得（必要に応じて作成）"""
        if not KAFKA_AVAILABLE:
            raise RuntimeError(
                "Kafka is not available. Please install kafka-python and six packages."
            )
        if self._admin is None:
            self._admin = KafkaAdminClient(
                bootstrap_servers=self.bootstrap_servers, client_id=self.client_id
            )
        return self._admin

    def list_topics(self) -> List[str]:
        """トピック一覧を取得"""
        try:
            admin = self._get_admin()
            metadata = admin.describe_topics()
            return list(metadata.keys())
        except KafkaError as e:
            raise Exception(f"Failed to list topics: {str(e)}")

    def create_topic(
        self, topic_name: str, num_partitions: int = 1, replication_factor: int = 1
    ) -> bool:
        """トピックを作成"""
        try:
            admin = self._get_admin()
            topic = NewTopic(
                name=topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor,
            )
            admin.create_topics([topic])
            return True
        except KafkaError as e:
            if "already exists" in str(e).lower():
                return False
            raise Exception(f"Failed to create topic: {str(e)}")

    def delete_topic(self, topic_name: str) -> bool:
        """トピックを削除"""
        try:
            admin = self._get_admin()
            admin.delete_topics([topic_name])
            return True
        except KafkaError as e:
            raise Exception(f"Failed to delete topic: {str(e)}")

    def publish_event(
        self,
        topic: str,
        event_type: str,
        data: Dict[str, Any],
        key: Optional[str] = None,
    ) -> bool:
        """イベントを発行"""
        try:
            producer = self._get_producer()
            event = {
                "event_type": event_type,
                "data": data,
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0",
            }

            future = producer.send(topic, value=event, key=key)
            # 送信完了を待つ（オプション）
            # future.get(timeout=10)
            return True
        except KafkaError as e:
            raise Exception(f"Failed to publish event: {str(e)}")

    def consume_events(
        self,
        topic: str,
        group_id: str,
        auto_offset_reset: str = "earliest",
        max_messages: int = 10,
    ) -> List[Dict[str, Any]]:
        """イベントを消費"""
        try:
            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                group_id=group_id,
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                key_deserializer=lambda k: k.decode("utf-8") if k else None,
                auto_offset_reset=auto_offset_reset,
                enable_auto_commit=True,
                consumer_timeout_ms=5000,  # 5秒でタイムアウト
            )

            messages = []
            for message in consumer:
                messages.append(
                    {
                        "topic": message.topic,
                        "partition": message.partition,
                        "offset": message.offset,
                        "key": message.key,
                        "value": message.value,
                        "timestamp": message.timestamp,
                    }
                )
                if len(messages) >= max_messages:
                    break

            consumer.close()
            return messages
        except KafkaError as e:
            raise Exception(f"Failed to consume events: {str(e)}")

    def get_topic_info(self, topic_name: str) -> Dict[str, Any]:
        """トピック情報を取得"""
        try:
            admin = self._get_admin()
            metadata = admin.describe_topics([topic_name])

            if topic_name not in metadata:
                raise Exception(f"Topic {topic_name} not found")

            topic_metadata = metadata[topic_name]
            return {
                "name": topic_name,
                "partitions": len(topic_metadata.partitions),
                "replication_factor": len(topic_metadata.partitions[0].replicas)
                if topic_metadata.partitions
                else 0,
            }
        except KafkaError as e:
            raise Exception(f"Failed to get topic info: {str(e)}")

    def close(self):
        """リソースを解放"""
        if self._producer:
            self._producer.close()
        if self._admin:
            self._admin.close()
