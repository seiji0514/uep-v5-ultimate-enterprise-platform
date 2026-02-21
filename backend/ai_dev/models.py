"""
AI支援開発関連のデータモデル
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class CodeGenerateRequest(BaseModel):
    """コード生成リクエスト"""

    description: str
    language: str = "python"
    framework: Optional[str] = None
    requirements: Optional[List[str]] = None


class TestSuiteCreate(BaseModel):
    """テストスイート作成モデル"""

    name: str
    description: Optional[str] = None
    test_cases: Optional[List[Dict[str, Any]]] = None


class TestRunRequest(BaseModel):
    """テスト実行リクエスト"""

    suite_id: str
    test_cases: Optional[List[str]] = None


class CodeReviewRequest(BaseModel):
    """コードレビューリクエスト"""

    code: str
    language: str = "python"
    check_style: bool = True
    check_security: bool = True
    check_performance: bool = True


class DocumentationRequest(BaseModel):
    """ドキュメント生成リクエスト"""

    doc_type: str  # api, readme, comments
    content: str
    language: str = "python"
    project_name: Optional[str] = None
    features: Optional[List[str]] = None
