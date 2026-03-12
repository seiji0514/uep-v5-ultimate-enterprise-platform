# 医療系スタンドアロンシステム

UEP v5.0 から独立した個人プロジェクト。医療系専門システムのプロトタイプ。

## 技術スタック

- Python 3.11+, FastAPI
- FHIR風API、AI診断サンプル、バイタルサイン

## 起動

```bash
cd projects/medical-standalone
pip install -r requirements.txt
python main.py
```

- API: http://localhost:8001
- ダッシュボード: http://localhost:8001/dashboard

## 注意

サンプルデータのみ使用。実患者データは使用していません。
