# 衛星軌道追跡システム - 使用方法

作成日: 2025年11月2日  
バージョン: 1.0.0（企業レベル）

---

## 📋 目次

1. [クイックスタート](#クイックスタート)
2. [サーバー起動](#サーバー起動)
3. [API使用方法](#api使用方法)
4. [テスト実行](#テスト実行)
5. [Docker使用](#docker使用)
6. [面談デモ方法](#面談デモ方法)

---

## 🚀 クイックスタート

### **必要環境**
- Python 3.11+ (現在: 3.13.5)
- pip
- (オプション) Docker Desktop

### **インストール**

```bash
# 1. ディレクトリ移動
cd satellite-orbit-tracker

# 2. 依存関係インストール（既にインストール済み）
pip install numpy fastapi uvicorn pydantic python-dateutil pytest pydantic-settings httpx

# 3. 動作確認
pytest test_api.py -v
```

---

## 🎯 サーバー起動

### **方法1: 通常起動**

```bash
# サーバー起動
python api_server_enterprise.py
```

**起動確認:**
```
============================================================
衛星軌道追跡システム - FastAPI REST API（企業レベル）
============================================================
Version: 1.0.0
Log Level: INFO
🚀 サーバー起動中...

API エンドポイント:
  - http://0.0.0.0:8000/
  - http://0.0.0.0:8000/iss/current
  - http://0.0.0.0:8000/iss/predict
  - http://0.0.0.0:8000/docs (Swagger UI)
  - http://0.0.0.0:8000/demo (3D可視化ダッシュボード)

============================================================
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### **方法2: バックグラウンド起動**

```bash
# Windows (PowerShell)
Start-Process python -ArgumentList "api_server_enterprise.py" -WindowStyle Hidden

# Linux/Mac
nohup python api_server_enterprise.py > server.log 2>&1 &
```

---

## 📡 API使用方法

### **1. ブラウザで確認**

#### **Swagger UI（対話的APIドキュメント）**
```
http://localhost:8000/docs
```

#### **ReDoc（読みやすいドキュメント）**
```
http://localhost:8000/redoc
```

#### **3D可視化ダッシュボード**
```
http://localhost:8000/demo
```

---

### **2. curlコマンドで使用**

#### **ヘルスチェック**
```bash
curl http://localhost:8000/health
```

**レスポンス:**
```json
{
  "status": "healthy",
  "service": "Satellite Orbit Tracker API",
  "version": "1.0.0",
  "timestamp": "2025-11-02T10:00:00.000000",
  "endpoints_available": 8,
  "log_level": "INFO"
}
```

#### **ISS現在位置取得**
```bash
curl http://localhost:8000/iss/current
```

**レスポンス:**
```json
{
  "timestamp": "2025-11-02T10:00:00.000000",
  "satellite": "ISS",
  "position_eci": {
    "x": 1234.56,
    "y": -789.01,
    "z": 6543.21
  },
  "velocity_eci": {
    "vx": 7.5,
    "vy": -2.3,
    "vz": 0.8
  },
  "geographic": {
    "lat": 35.6,
    "lon": 139.7,
    "alt": 420.0
  }
}
```

#### **ISS軌道予測（24時間）**
```bash
curl -X POST http://localhost:8000/iss/predict \
  -H "Content-Type: application/json" \
  -d '{"duration_hours": 24.0, "step_minutes": 5.0}'
```

#### **ISS軌道予測（カスタム期間）**
```bash
curl -X POST http://localhost:8000/iss/predict \
  -H "Content-Type: application/json" \
  -d '{"duration_hours": 12.0, "step_minutes": 10.0}'
```

#### **カスタム軌道計算**
```bash
curl -X POST http://localhost:8000/orbit/calculate \
  -H "Content-Type: application/json" \
  -d '{
    "semi_major_axis": 6791.0,
    "eccentricity": 0.0003,
    "inclination": 51.6,
    "raan": 0.0,
    "arg_perigee": 0.0,
    "mean_anomaly": 0.0,
    "duration_hours": 24.0
  }'
```

#### **衛星リスト取得**
```bash
curl http://localhost:8000/satellites/list
```

---

### **3. Pythonスクリプトで使用**

```python
import requests

# ベースURL
BASE_URL = "http://localhost:8000"

# 1. ヘルスチェック
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# 2. ISS現在位置
response = requests.get(f"{BASE_URL}/iss/current")
iss_data = response.json()
print(f"ISS位置: 緯度{iss_data['geographic']['lat']:.2f}°, "
      f"経度{iss_data['geographic']['lon']:.2f}°, "
      f"高度{iss_data['geographic']['alt']:.2f}km")

# 3. ISS軌道予測
response = requests.post(f"{BASE_URL}/iss/predict", json={
    "duration_hours": 24.0,
    "step_minutes": 5.0
})
orbit_data = response.json()
print(f"予測ポイント数: {orbit_data['data_points']}")

# 4. カスタム軌道計算
response = requests.post(f"{BASE_URL}/orbit/calculate", json={
    "semi_major_axis": 7000.0,
    "eccentricity": 0.001,
    "inclination": 45.0,
    "raan": 0.0,
    "arg_perigee": 0.0,
    "mean_anomaly": 0.0,
    "duration_hours": 12.0
})
custom_orbit = response.json()
print(f"カスタム軌道ポイント数: {custom_orbit['data_points']}")
```

---

## 🧪 テスト実行

### **全テスト実行**
```bash
pytest test_api.py -v
```

**結果:**
```
============================= test session starts =============================
collected 13 items

test_api.py::TestGeneralEndpoints::test_root_endpoint PASSED             [  7%]
test_api.py::TestGeneralEndpoints::test_health_check PASSED              [ 15%]
test_api.py::TestISSEndpoints::test_iss_current_position PASSED          [ 23%]
... (省略)
======================= 13 passed, 24 warnings in 4.66s =======================
```

### **カバレッジ付きテスト**
```bash
pytest test_api.py --cov=. --cov-report=html
```

### **特定のテストのみ実行**
```bash
# ISSエンドポイントのみ
pytest test_api.py::TestISSEndpoints -v

# 特定のテスト1つ
pytest test_api.py::TestISSEndpoints::test_iss_current_position -v
```

---

## 🐳 Docker使用（準備済み）

### **前提条件**
Docker Desktop for Windows のインストールが必要  
https://www.docker.com/products/docker-desktop

### **Docker起動**

```bash
# 1. イメージビルド & 起動
docker-compose up -d

# 2. ログ確認
docker-compose logs -f api

# 3. コンテナ状態確認
docker-compose ps

# 4. 停止
docker-compose down
```

### **Docker環境でのAPI使用**

サーバー起動後、同じURLでアクセス可能：
```
http://localhost:8000/health
http://localhost:8000/iss/current
http://localhost:8000/docs
```

### **監視ツール（Dockerのみ）**

- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)

---

## 🎬 面談デモ方法

### **準備（面談前）**

1. **サーバー起動**
   ```bash
   python api_server_enterprise.py
   ```

2. **ブラウザで開く（複数タブ）**
   - タブ1: Swagger UI - `http://localhost:8000/docs`
   - タブ2: 3D可視化 - `http://localhost:8000/demo`
   - タブ3: コードエディタ（VSCode等）

3. **PowerShellターミナル準備**
   - `curl` コマンド履歴準備
   - `pytest` 実行準備

---

### **デモシナリオ（15分）**

#### **1. システム概要説明（2分）**
```
「11月1日に約1時間半で基礎実装、
 11月2日に約2時間で企業レベルに改善しました。」

画面: README_ENTERPRISE.md を表示
```

#### **2. ライブテスト実行（2分）**
```bash
pytest test_api.py -v
```
```
「13テスト全てPASS、4.66秒で完了。
 正常系・異常系・バリデーション全て検証済みです。」
```

#### **3. API実行デモ（3分）**

**Swagger UIで実行:**
1. `/health` - ヘルスチェック
2. `/iss/current` - ISS現在位置
3. `/iss/predict` - 24時間軌道予測

```
「Swagger UIで対話的にAPIを実行できます。
 エラーハンドリングも実装済みです。」
```

#### **4. コード説明（3分）**

**見せるファイル:**
- `api_server_enterprise.py` - エラーハンドリング、ロギング
- `config.py` - 環境変数管理
- `test_api.py` - テストコード

```
「企業レベルの機能を実装しています：
 - グローバル例外ハンドラ
 - 構造化ログ
 - 環境変数管理
 - 型安全なバリデーション」
```

#### **5. 拡充ロードマップ説明（3分）**

**見せるファイル:**
- `README_ENTERPRISE.md` - Phase 1-3のロードマップ
- `ENTERPRISE_UPGRADE_SUMMARY.md` - 実装詳細

```
「3-6ヶ月で完全な企業レベルに到達できる
 明確なロードマップがあります：
 - Phase 1: 精度検証（1-2ヶ月）
 - Phase 2: AWS統合（1-2ヶ月）
 - Phase 3: 規制対応（1-2ヶ月）」
```

#### **6. 質疑応答（2分）**
```
想定質問:
Q1: 「なぜこんなに速く実装できるの？」
A1: 「少林寺拳法で培った超高速学習能力と、
     AI協働開発の活用です。」

Q2: 「本当に企業で使えるの？」
A2: 「現在は技術デモ・PoCレベルですが、
     基礎技術の理解と実装能力は証明済みです。
     Fusicチームと協力して実用レベルに
     引き上げられます。」

Q3: 「AWSとの統合は？」
A3: 「config.py に AWS設定を準備済みです。
     Ground Station SDKの統合は
     Phase 2で実装予定です。」
```

---

## 📊 ログ確認

### **ログファイル**
```bash
# ログディレクトリ作成（初回のみ）
mkdir logs

# ログ確認
tail -f logs/satellite_tracker.log
```

### **ログ内容例**
```
2025-11-02 10:00:00 - satellite_tracker - INFO - Root endpoint accessed
2025-11-02 10:00:01 - satellite_tracker - INFO - ISS current position request received
2025-11-02 10:00:01 - satellite_tracker - INFO - ISS position calculated in 15.23ms
2025-11-02 10:00:05 - satellite_tracker - INFO - ISS orbit prediction request: duration=24.0h, step=5.0min
2025-11-02 10:00:06 - satellite_tracker - INFO - Orbit Calculation: ISS | Duration: 24.0h | Points: 289 | Calc Time: 1234.56ms
```

---

## 🛠️ トラブルシューティング

### **ポート8000が使用中**
```bash
# Windowsでポート確認
netstat -ano | findstr :8000

# プロセス終了
taskkill /PID <PID> /F

# または別ポート使用（config.py で PORT を変更）
```

### **依存関係エラー**
```bash
# 依存関係再インストール
pip install --upgrade numpy fastapi uvicorn pydantic python-dateutil pytest pydantic-settings httpx
```

### **テスト失敗**
```bash
# 詳細なエラー表示
pytest test_api.py -v --tb=long

# キャッシュクリア
pytest --cache-clear test_api.py -v
```

---

## 📁 ファイル構成

```
satellite-orbit-tracker/
├── api_server_enterprise.py    # ✅ FastAPI アプリケーション（企業レベル）
├── orbit_calculator.py          # ✅ 軌道計算エンジン
├── config.py                    # ✅ 設定管理
├── logger.py                    # ✅ ロギング設定
├── test_api.py                  # ✅ APIテスト
├── Dockerfile                   # ✅ Docker イメージ定義
├── docker-compose.yml           # ✅ Docker Compose 設定
├── requirements.txt             # ✅ Python 依存関係（基本）
├── requirements_enterprise.txt  # ✅ Python 依存関係（企業レベル）
├── env.template                 # ✅ 環境変数テンプレート
├── README_ENTERPRISE.md         # ✅ 企業レベル実装ガイド
├── ENTERPRISE_UPGRADE_SUMMARY.md # ✅ 実装サマリー
├── AUTOMATED_TEST_RESULTS.md    # ✅ テスト結果
├── USAGE_GUIDE.md               # ✅ 本ファイル
├── .github/
│   └── workflows/
│       └── ci.yml               # ✅ CI/CD パイプライン
├── logs/                        # ログファイル
└── monitoring/                  # 監視設定
    └── prometheus.yml           # ✅ Prometheus 設定
```

---

## 🎯 よく使うコマンド集

```bash
# サーバー起動
python api_server_enterprise.py

# テスト実行
pytest test_api.py -v

# API確認
curl http://localhost:8000/health
curl http://localhost:8000/iss/current

# ログ確認
tail -f logs/satellite_tracker.log

# Docker起動（Docker Desktop インストール済みの場合）
docker-compose up -d
docker-compose logs -f api
docker-compose down

# ブラウザで開く
start http://localhost:8000/docs       # Swagger UI
start http://localhost:8000/redoc      # ReDoc
start http://localhost:8000/demo       # 3D可視化
```

---

## 📞 サポート

質問・要望がございましたら、お気軽にお問い合わせください。

**開発者**: 小川清志  
**Email**: kaho052514@gmail.com  
**作成日**: 2025年11月2日

---

**企業レベル実装完了！** 🎉  
**面談でのデモンストレーション準備完璧です！** 💪

