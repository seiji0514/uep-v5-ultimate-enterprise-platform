# 統合監視・オブザーバビリティ基盤

**作成日**: 2026年1月29日  
**Phase**: 1.5

---

## 📋 概要

UEP v5.0の統合監視・オブザーバビリティ基盤は、以下の機能を提供します：

- **メトリクス収集**: Prometheus
- **可視化**: Grafana
- **ログ管理**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **分散トレーシング**: OpenTelemetry

---

## 🏗️ アーキテクチャ

```
infrastructure/monitoring/
├── README.md            # このファイル
├── prometheus/
│   └── prometheus.yml   # Prometheus設定
└── grafana/
    ├── dashboards/      # Grafanaダッシュボード
    └── datasources/     # Grafanaデータソース

backend/monitoring/
├── __init__.py          # モジュール初期化
├── metrics.py           # メトリクス収集
├── logging.py           # ログ管理
├── tracing.py           # 分散トレーシング
└── routes.py            # 監視APIエンドポイント
```

---

## 🔧 サービス設定

### Prometheus

- **URL**: http://localhost:9090
- **設定ファイル**: `infrastructure/monitoring/prometheus/prometheus.yml`
- **メトリクスエンドポイント**: `/metrics`

### Grafana

- **URL**: http://localhost:3000
- **ユーザー名**: `admin`
- **パスワード**: `admin`
- **データソース**: Prometheus (自動設定)

### Elasticsearch

- **URL**: http://localhost:9200
- **用途**: ログストレージ

### Logstash

- **用途**: ログ処理・変換

### Kibana

- **URL**: http://localhost:5601
- **用途**: ログ可視化

---

## 📝 APIエンドポイント

### 監視

- `GET /api/v1/monitoring/metrics` - メトリクス取得
- `GET /api/v1/monitoring/health` - ヘルスチェック
- `GET /api/v1/monitoring/logs` - ログ取得
- `GET /api/v1/monitoring/traces` - トレース取得

---

## 🚀 使用方法

### Prometheusでメトリクス確認

```bash
# Prometheus UIにアクセス
# http://localhost:9090

# メトリクスクエリ例
up{job="backend-api"}
http_requests_total
```

### Grafanaでダッシュボード確認

```bash
# Grafana UIにアクセス
# http://localhost:3000 (admin/admin)
```

### Kibanaでログ確認

```bash
# Kibana UIにアクセス
# http://localhost:5601
```

---

## 📚 参考資料

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [ELK Stack Documentation](https://www.elastic.co/guide/)
- [OpenTelemetry Documentation](https://opentelemetry.io/docs/)

---

以上
