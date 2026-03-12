# UEP v5.0 拡張実装一覧（ENHANCEMENTS_EXTENDED）

**作成日**: 2026年3月  
**参照**: [UEP_v5_追加スキル・技術案.md](UEP_v5_追加スキル・技術案.md)

---

## 1. 既存補強スキル拡張

### 1.1 Go（uep-cli / uep-operator）

| 項目 | パス | 内容 |
|------|------|------|
| gRPC サブコマンド | `tools/uep-cli/cmd/grpc.go` | `uep-cli grpc status` で gRPC 疎通確認 |
| uep-operator | `tools/uep-operator/` | Kubernetes Operator スケルトン（main.go, go.mod, README） |

**ビルド**:
```bash
cd tools/uep-cli && go build -o uep-cli .
cd tools/uep-operator && go build -o uep-operator .
```

### 1.2 eBPF

| 項目 | パス | 内容 |
|------|------|------|
| Cilium 設定 | `infrastructure/falco/cilium-config.yaml` | eBPF CNI、Hubble 可観測性 |
| カスタムトレース | `tools/ebpf/custom_trace.bt` | openat トレース、/etc/passwd 等のセキュリティ検知 |

**実行**: `sudo bpftrace tools/ebpf/custom_trace.bt`

### 1.3 GraphQL

| 項目 | パス | 内容 |
|------|------|------|
| バッチリゾルバ | `backend/graphql_api/batch_resolver.py` | user_loader, project_loader |
| キャッシュ | `backend/graphql_api/cache.py` | インメモリキャッシュ、TTL、無効化 |

### 1.4 分散トレーシング

| 項目 | パス | 内容 |
|------|------|------|
| サンプリング | `backend/monitoring/tracing.py` | OTEL_TRACES_SAMPLER, OTEL_TRACES_SAMPLER_ARG 対応 |

**環境変数**: `OTEL_TRACES_SAMPLER=parentbased_traceidratio`, `OTEL_TRACES_SAMPLER_ARG=0.1`（10%サンプリング）

### 1.5 イベント駆動

| 項目 | パス | 内容 |
|------|------|------|
| デッドレターキュー | `backend/event_streaming/dead_letter_queue.py` | push_to_dlq, list_dlq, dlq_stats |
| リトライポリシー | `backend/event_streaming/retry_policy.py` | RetryPolicy, retry_with_policy, retry_async |

---

## 2. 追加スキル（高・中・低）

### 2.1 Terraform

| 項目 | パス | 内容 |
|------|------|------|
| メイン | `infrastructure/terraform/main.tf` | EKS 参照、AWS/K8s プロバイダー |
| 変数 | `infrastructure/terraform/variables.tf` | project_name, environment, aws_region |
| EKS モジュール | `infrastructure/terraform/modules/eks/` | スケルトン |

### 2.2 Argo CD

| 項目 | パス | 内容 |
|------|------|------|
| Application | `infrastructure/argocd/application.yaml` | GitOps デプロイ定義 |

### 2.3 FinOps

| 項目 | パス | 内容 |
|------|------|------|
| FinOps モジュール | `backend/optimization/finops.py` | get_cost_summary, get_cost_by_tag |
| API | `backend/optimization/routes.py` | `/api/v1/optimization/finops/cost-summary`, `cost-by-tag` |

### 2.4 Redis Streams

| 項目 | パス | 内容 |
|------|------|------|
| クライアント | `backend/event_streaming/redis_streams.py` | RedisStreamsClient（add, read, create_consumer_group） |

### 2.5 LangGraph

| 項目 | パス | 内容 |
|------|------|------|
| エージェント | `backend/generative_ai/langgraph_agent.py` | create_agent_graph, run_agent（スケルトン） |

### 2.6 tRPC

| 項目 | パス | 内容 |
|------|------|------|
| ルーター | `backend/core/trpc_router.py` | TRPCRouter, query/mutation デコレータ |

### 2.7 WebAssembly (WASM)

| 項目 | パス | 内容 |
|------|------|------|
| README | `tools/wasm/README.md` | wasm-pack, Rust ビルド手順 |

---

## 3. ドメイン拡張

### 3.1 FinTech

| 項目 | パス | 内容 |
|------|------|------|
| ストレステスト | `backend/fintech/stress_test.py` | run_stress_test, StressScenario |
| API | `backend/fintech/routes.py` | `GET /api/v1/fintech/stress-test` |

### 3.2 医療 (Medical)

| 項目 | パス | 内容 |
|------|------|------|
| FHIR クライアント | `backend/medical/fhir_client.py` | FHIRClient, get_patient, search_observations |
| API | `backend/medical/routes.py` | `GET /api/v1/medical/fhir/patient/{id}`, `fhir/observations/{id}` |

### 3.3 製造 (Manufacturing)

| 項目 | パス | 内容 |
|------|------|------|
| OPC-UA クライアント | `backend/manufacturing/opcua_client.py` | OPCUAClient, read_node, browse_nodes |
| API | `backend/manufacturing/routes.py` | `GET /api/v1/manufacturing/opcua/read/{node_id}`, `opcua/browse` |

### 3.4 サイバー防衛

| 項目 | パス | 内容 |
|------|------|------|
| SOAR 連携 | `backend/cyber_defense/soar_integration.py` | execute_playbook, get_available_playbooks |
| API | `backend/cyber_defense/routes.py` | `GET /api/v1/cyber-defense/soar/playbooks`, `POST soar/execute` |

---

## 4. フロントエンド

| 技術 | パス | 内容 |
|------|------|------|
| TanStack React Query | `frontend/src/lib/queryClient.ts`, `App.tsx` | QueryClientProvider |
| Zustand | `frontend/src/store/useAppStore.ts` | グローバル状態（sidebarOpen, language） |
| Storybook | `frontend/.storybook/`, `Button.stories.tsx` | コンポーネントカタログ |
| Playwright | `frontend/playwright.config.ts`, `e2e/smoke.spec.ts` | E2E テスト |
| i18n | `frontend/src/i18n/index.ts` | react-i18next（ja/en） |
| PWA | `frontend/src/lib/pwa-register.ts` | Service Worker 登録 |
| Web Vitals | `frontend/src/lib/webVitals.ts`, `reportWebVitals.ts` | パフォーマンス計測 |

**コマンド**:
- `npm run storybook` - Storybook 起動
- `npm run test:e2e` - Playwright E2E

---

## 5. インフラ・DevOps

| 技術 | パス | 内容 |
|------|------|------|
| HPA/VPA | `infrastructure/kubernetes/hpa-vpa/` | hpa-backend.yaml, vpa-backend.yaml |
| NetworkPolicy | `infrastructure/kubernetes/network-policy/` | backend-policy.yaml |
| Thanos | `infrastructure/monitoring/thanos/` | values.yaml（S3 長期保存） |
| Vault 拡張 | `backend/security/vault_client.py` | create_dynamic_secret, transit_encrypt/decrypt |
| Crossplane | `infrastructure/crossplane/` | provider-config.yaml |
| Kyverno | `infrastructure/kyverno/` | policy-disallow-privileged.yaml |

---

## 6. 依存関係

### バックエンド（オプショナル）

- `redis` - Redis Streams
- `fhirclient` - FHIR クライアント
- `opcua` - OPC-UA
- `langgraph`, `langchain` - LangGraph エージェント

### フロントエンド

- `@tanstack/react-query`
- `zustand`
- `i18next`, `react-i18next`
- `workbox-window`
- `@storybook/*`, `@playwright/test`

---

## 7. 参照

- [ENHANCEMENTS.md](ENHANCEMENTS.md) - 既存補強スキル
- [UEP_v5_追加スキル・技術案.md](UEP_v5_追加スキル・技術案.md) - 追加案一覧
- [参画に必要なこと.md](参画に必要なこと.md) - 参画前提条件
