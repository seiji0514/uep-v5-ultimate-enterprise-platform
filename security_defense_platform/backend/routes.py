"""
統合セキュリティ・防衛プラットフォーム API
セキュリティコマンドセンター + サイバー対策（IDS/IPS, EDR, SIEM, 脅威インテリジェンス, コンプライアンス）
"""
import sys
import os
# プロジェクトルートを path に追加（backend.security_center のため）
_project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)
# backend を path に追加（security_center のため）
_backend = os.path.join(_project_root, "backend")
if _backend not in sys.path:
    sys.path.insert(0, _backend)

from security_center.routes import router

__all__ = ["router"]
