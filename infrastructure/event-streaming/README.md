# 統合イベントストリーミング

**作成日**: 2026年1月29日  
**Phase**: 1.4

---

## 📋 概要

UEP v5.0の統合イベントストリーミングは、Apache Kafkaを使用して以下の機能を提供します：

- **イベントストリーミング**: リアルタイムイベント処理
- **Event Sourcing**: イベントソーシングパターン
- **CQRS**: Command Query Responsibility Segregationパターン

---

## 🏗️ アーキテクチャ

```
infrastructure/event-streaming/
├── README.md            # このファイル
└── kafka-config/        # Kafka設定（将来）

backend/event_streaming/
├── __init__.py          # モジュール初期化
├── kafka_client.py      # Kafkaクライアント
├── event_sourcing.py    # Event Sourcing実装
├── cqrs.py              # CQRS実装
├── models.py            # イベントモデル
└── routes.py            # APIエンドポイント
```

---

## 🔧 Kafka設定

### 接続情報

- **Broker**: `localhost:9092` (外部) / `kafka:9092` (内部)
- **Zookeeper**: `zookeeper:2181`

### トピック構成

- `user-events`: ユーザー関連イベント
- `data-lake-events`: データレイク関連イベント
- `mlops-events`: MLOps関連イベント
- `security-events`: セキュリティ関連イベント
- `system-events`: システム関連イベント

---

## 📝 APIエンドポイント

### イベントストリーミング

- `GET /api/v1/events/topics` - トピック一覧
- `POST /api/v1/events/topics` - トピック作成
- `POST /api/v1/events/publish` - イベント発行
- `GET /api/v1/events/consume` - イベント消費
- `GET /api/v1/events/history` - イベント履歴

### Event Sourcing

- `POST /api/v1/events/commands` - コマンド送信
- `GET /api/v1/events/aggregates/{aggregate_id}` - 集約状態取得
- `GET /api/v1/events/aggregates/{aggregate_id}/events` - 集約イベント履歴

### CQRS

- `POST /api/v1/events/commands` - コマンド送信（書き込み）
- `GET /api/v1/events/queries` - クエリ実行（読み取り）

---

## 🚀 使用方法

### Kafkaへの接続

```python
from event_streaming.kafka_client import KafkaClient

client = KafkaClient(bootstrap_servers="kafka:9092")
```

### イベント発行

```bash
curl -X POST "http://localhost:8000/api/v1/events/publish" \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "user-events",
    "event_type": "user.created",
    "data": {"user_id": "123", "username": "testuser"}
  }'
```

### イベント消費

```bash
curl -X GET "http://localhost:8000/api/v1/events/consume?topic=user-events&group_id=my-group" \
  -H "Authorization: Bearer <access_token>"
```

---

## 📚 参考資料

- [Apache Kafka Documentation](https://kafka.apache.org/documentation/)
- [Event Sourcing Pattern](https://martinfowler.com/eaaDev/EventSourcing.html)
- [CQRS Pattern](https://martinfowler.com/bliki/CQRS.html)

---

以上
