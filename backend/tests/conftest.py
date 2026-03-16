"""pytest 共通設定"""
import os
import sys

# テスト時は docs/openapi を有効化するため development をデフォルトに
os.environ.setdefault("ENVIRONMENT", "development")

# backend をパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
