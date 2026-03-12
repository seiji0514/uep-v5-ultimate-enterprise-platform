# 宇宙系スタンドアロンシステム

UEP v5.0 から独立した個人プロジェクト。宇宙・衛星データ可視化のプロトタイプ。

## 技術スタック

- Python 3.11+, FastAPI
- 衛星軌道、打ち上げ予定、NASA APOD風API

## 起動

```bash
cd projects/space-standalone
pip install -r requirements.txt
python main.py
```

- API: http://localhost:8003
- ダッシュボード: http://localhost:8003/dashboard

## 拡張

- NASA API: https://api.nasa.gov （APIキー取得で実データ連携可能）
- 衛星TLE: CelesTrak等の公開データ
