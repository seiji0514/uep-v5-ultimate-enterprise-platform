# スタンドアロンプロジェクト（UEP v5.0 から独立）

医療系・航空系・宇宙系の個人プロジェクト。UEP v5.0 本体とは独立して動作します。

## プロジェクト一覧

| プロジェクト | ポート | 説明 |
|-------------|--------|------|
| **unified-platform** | 8000 | **医療+航空+宇宙 統合**（Phase 1-5: DB, Docker, Redis, Auth, K8s, CI/CD, 監視） |
| 医療系 | 8001 | FHIR風API、AI診断サンプル、バイタルサイン |
| 航空系 | 8002 | フライトデータ、空港統計、遅延分析 |
| 宇宙系 | 8003 | 衛星データ、打ち上げ予定、NASA APOD風 |

## 起動方法

```bash
# 統合プラットフォーム（推奨）
cd projects/unified-platform && docker compose up -d

# 医療系
cd projects/medical-standalone && pip install -r requirements.txt && python main.py

# 航空系
cd projects/aviation-standalone && pip install -r requirements.txt && python main.py

# 宇宙系
cd projects/space-standalone && pip install -r requirements.txt && python main.py
```

## 同時起動

```bash
# 医療系（バックグラウンド）
cd projects/medical-standalone && python main.py &

# 航空系（バックグラウンド）
cd projects/aviation-standalone && python main.py &

# 宇宙系（バックグラウンド）
cd projects/space-standalone && python main.py &
```

- 医療: http://localhost:8001
- 航空: http://localhost:8002
- 宇宙: http://localhost:8003
