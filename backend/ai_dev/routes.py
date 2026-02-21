"""
AI支援開発APIエンドポイント
"""
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from auth.jwt_auth import get_current_active_user
from auth.rbac import require_permission

from .code_generation import code_generator
from .code_review import CodeReview, code_reviewer
from .documentation import documentation_generator
from .models import (
    CodeGenerateRequest,
    CodeReviewRequest,
    DocumentationRequest,
    TestRunRequest,
    TestSuiteCreate,
)
from .test_automation import test_automation

router = APIRouter(prefix="/api/v1/ai-dev", tags=["AI支援開発"])


@router.post("/code/generate")
@require_permission("read")
async def generate_code(
    request: CodeGenerateRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """コードを生成"""
    result = await code_generator.generate_code(
        description=request.description,
        language=request.language,
        framework=request.framework,
        requirements=request.requirements,
    )
    return result


@router.post("/code/generate-test")
@require_permission("read")
async def generate_test_code(
    code: str,
    language: str = "python",
    test_framework: Optional[str] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """テストコードを生成"""
    result = await code_generator.generate_test_code(
        code=code, language=language, test_framework=test_framework
    )
    return result


@router.post("/code/refactor")
@require_permission("read")
async def refactor_code(
    code: str,
    language: str = "python",
    improvements: Optional[List[str]] = None,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """コードをリファクタリング"""
    result = await code_generator.refactor_code(
        code=code, language=language, improvements=improvements
    )
    return result


@router.post("/tests/suites", status_code=status.HTTP_201_CREATED)
@require_permission("read")
async def create_test_suite(
    suite_data: TestSuiteCreate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """テストスイートを作成"""
    suite = test_automation.create_test_suite(
        name=suite_data.name,
        description=suite_data.description,
        test_cases=suite_data.test_cases,
    )
    return suite


@router.post("/tests/run")
@require_permission("read")
async def run_tests(
    request: TestRunRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """テストを実行"""
    try:
        result = await test_automation.run_tests(
            suite_id=request.suite_id, test_cases=request.test_cases
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/review", response_model=CodeReview)
@require_permission("read")
async def review_code(
    request: CodeReviewRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """コードをレビュー"""
    review = await code_reviewer.review_code(
        code=request.code,
        language=request.language,
        check_style=request.check_style,
        check_security=request.check_security,
        check_performance=request.check_performance,
    )
    return review


@router.post("/documentation/generate")
@require_permission("read")
async def generate_documentation(
    request: DocumentationRequest,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
):
    """ドキュメントを生成"""
    if request.doc_type == "api":
        result = await documentation_generator.generate_api_docs(
            code=request.content, language=request.language
        )
    elif request.doc_type == "readme":
        result = await documentation_generator.generate_readme(
            project_name=request.project_name or "Project",
            description=request.content,
            features=request.features,
        )
    elif request.doc_type == "comments":
        result = await documentation_generator.generate_code_comments(
            code=request.content, language=request.language
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid document type"
        )

    return result
