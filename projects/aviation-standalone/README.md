# 航空系スタンドアロンシステム

UEP v5.0 から独立した個人プロジェクト。航空系・地上システムのプロトタイプ。

## 技術スタック

- Python 3.11+, FastAPI
- フライトデータ分析、空港統計、遅延分析

## 起動

```bash
cd projects/aviation-standalone
pip install -r requirements.txt
python main.py
```

- API: http://localhost:8002
- ダッシュボード: http://localhost:8002/dashboard

## 注意

サンプルデータのみ。機体制御・安全クリティカルな部分は含みません。
