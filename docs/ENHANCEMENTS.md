# UEP v5.0 補強スキル実装一覧

## 1. Go CLI（uep-cli）

| 項目 | 内容 |
|------|------|
| cobra | サブコマンド構造（health, version, events, graphql） |
| 認証 | `--token` で JWT 指定 |
| 出力形式 | `--output json/table` |
| コマンド | `events list`, `events outbox`, `graphql query` |

**ビルド**: `cd tools/uep-cli && go build -o uep-cli.exe .`

---

## 2. eBPF（Falco / BCC / bpftrace）

| 項目 | 内容 |
|------|------|
| Falco ルール | `infrastructure/falco/falco_rules_uep.yaml` |
| Webhook | `POST /api/v1/security-center/falco/alerts` |
| bpftrace | `tools/ebpf/trace_open.bt` |
| BCC | `tools/ebpf/README.md` にサンプル |

**起動**: `docker-compose --profile security up falco`

---

## 3. GraphQL

| 項目 | 内容 |
|------|------|
| DataLoader | `service_detail(name)` で N+1 対策 |
| スキーマ拡張 | Project, User, projects, users |
| サブスクリプション | `health_updates`, `service_status`（WebSocket） |
| フェデレーション | `backend/graphql_api/federation.py` |

---

## 4. 分散トレーシング

| 項目 | 内容 |
|------|------|
| W3C Trace Context | traceparent, tracestate ヘッダー |
| カスタムスパン | `tracing_handler.span("name", attrs)` |
| Jaeger | http://localhost:16686 |

**詳細**: [docs/TRACING_JAEGER.md](TRACING_JAEGER.md)

---

## 5. イベント駆動

| 項目 | 内容 |
|------|------|
| Saga 補正 | `execute_step`, `compensate` |
| アウトボックス | `OutboxStore`, `create_outbox_event` |
| ポーリング | `outbox_poller.poll_and_publish_outbox` |
| Kafka Streams | `infrastructure/event-streaming/kafka-streams/` |

---

## 6. 全体

| 項目 | 内容 |
|------|------|
| E2E テスト | `backend/tests/test_e2e.py` |
| CI | `.github/workflows/ci-cd.yml`（Go ビルド追加） |
| ドキュメント | 本ファイル、TRACING_JAEGER.md 等 |
