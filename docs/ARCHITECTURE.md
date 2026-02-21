# UEP v5.0 アーキテクチャ図

**作成日**: 2026年2月  
**対象**: 次世代エンタープライズ統合プラットフォーム v5.0

---

## 1. システム全体構成

```mermaid
flowchart TB
    subgraph Client["クライアント層"]
        Web[Webブラウザ]
        API_Client[APIクライアント]
    end

    subgraph Gateway["API Gateway層"]
        Kong[Kong]
        Envoy[Envoy]
    end

    subgraph Backend["バックエンド層"]
        FastAPI[FastAPI]
        Auth[認証・認可]
        MLOps[MLOps]
        GenAI[生成AI]
        Security[セキュリティ]
        Chaos[Chaos Engineering]
        GraphQL[GraphQL]
    end

    subgraph Data["データ層"]
        PostgreSQL[(PostgreSQL)]
        Redis[(Redis)]
        MinIO[(MinIO)]
        Kafka[Kafka]
    end

    subgraph Monitor["監視層"]
        Prometheus[Prometheus]
        Grafana[Grafana]
        ELK[ELK Stack]
    end

    Web --> API_Client
    API_Client --> Kong
    Kong --> Envoy
    Envoy --> FastAPI
    FastAPI --> Auth
    FastAPI --> MLOps
    FastAPI --> GenAI
    FastAPI --> Security
    FastAPI --> Chaos
    FastAPI --> GraphQL
    FastAPI --> PostgreSQL
    FastAPI --> Redis
    FastAPI --> MinIO
    FastAPI --> Kafka
    FastAPI --> Prometheus
    Prometheus --> Grafana
```

---

## 2. レベル別アーキテクチャ

```mermaid
flowchart LR
    subgraph L1["Level 1: コア"]
        MLOps[MLOps]
        GenAI[生成AI]
        Sec[セキュリティ]
        Cloud[クラウドインフラ]
        IDOP[IDOP]
        AIDev[AI支援開発]
        Monitor[監視]
    end

    subgraph L2["Level 2: プラットフォーム"]
        SaaS[SaaS]
        Marketplace[APIマーケットプレイス]
    end

    subgraph L3["Level 3: エコシステム"]
        Partner[パートナー統合]
        ModelShare[モデル共有]
    end

    subgraph L4["Level 4: インダストリー"]
        InferenceAI[推論AI]
        MCP[MCP/A2A]
        Gov[ガバナンス]
    end

    subgraph L5["Level 5: グローバル"]
        MultiRegion[マルチリージョン]
        HA[高可用性]
        DR[災害復旧]
    end

    L1 --> L2 --> L3 --> L4 --> L5
```

---

## 3. 技術スタック構成

```mermaid
flowchart TB
    subgraph Frontend["フロントエンド"]
        React[React 18+]
        TS[TypeScript]
        MUI[Material-UI]
    end

    subgraph Backend["バックエンド"]
        Python[Python 3.11+]
        FastAPI[FastAPI]
        SQLAlchemy[SQLAlchemy]
    end

    subgraph API["API層"]
        REST[REST API]
        GraphQL[GraphQL]
        ChaosAPI[Chaos API]
    end

    subgraph Infra["インフラ"]
        Docker[Docker]
        K8s[Kubernetes]
        Terraform[Terraform]
    end

    subgraph Quality["品質保証"]
        Locust[Locust 負荷テスト]
        Contract[Contract Testing]
        Pytest[Pytest]
    end

    React --> REST
    React --> GraphQL
    React --> ChaosAPI
    FastAPI --> REST
    FastAPI --> GraphQL
    FastAPI --> ChaosAPI
    Quality --> Backend
```

---

## 4. データフロー（認証）

```mermaid
sequenceDiagram
    participant C as クライアント
    participant A as FastAPI
    participant JWT as JWT検証
    participant DB as データベース

    C->>A: POST /api/v1/auth/login
    A->>DB: ユーザー照合
    DB-->>A: ユーザー情報
    A->>A: トークン生成
    A-->>C: access_token

    C->>A: GET /api/v1/xxx (Bearer token)
    A->>JWT: トークン検証
    JWT-->>A: 検証OK
    A->>DB: データ取得
    DB-->>A: 結果
    A-->>C: レスポンス
```

---

## 5. Chaos Engineering フロー

```mermaid
flowchart LR
    UI[Chaos UI] -->|遅延注入| API[/api/v1/chaos/delay]
    UI -->|エラー注入| API2[/api/v1/chaos/error]
    UI -->|混合| API3[/api/v1/chaos/mixed]
    API --> Backend[FastAPI]
    API2 --> Backend
    API3 --> Backend
    Backend -->|asyncio.sleep| Delay[遅延]
    Backend -->|HTTPException| Error[エラー]
```

---

## 6. ファイル構成（主要）

| ディレクトリ | 説明 |
|-------------|------|
| `backend/` | FastAPI バックエンド |
| `backend/chaos/` | Chaos Engineering モジュール |
| `backend/graphql_api/` | GraphQL モジュール |
| `backend/tests/contract/` | Contract Testing |
| `frontend/` | React フロントエンド |
| `frontend/src/components/Chaos/` | Chaos UI |
| `infrastructure/` | インフラ設定 |
| `scripts/` | ユーティリティスクリプト |

---

以上
