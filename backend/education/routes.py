"""
教育 APIエンドポイント
LMS、学習進捗、成績、教材管理
"""
from datetime import datetime, timedelta
from typing import Any, Dict, List

from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/education", tags=["教育"])


def _courses() -> List[Dict[str, Any]]:
    return [
        {
            "id": "c-001",
            "title": "Python基礎",
            "status": "開講中",
            "enrolled": 45,
            "completion_rate": 0.78,
        },
        {
            "id": "c-002",
            "title": "データ分析入門",
            "status": "開講中",
            "enrolled": 32,
            "completion_rate": 0.65,
        },
        {
            "id": "c-003",
            "title": "AI/ML実践",
            "status": "開講中",
            "enrolled": 28,
            "completion_rate": 0.52,
        },
        {
            "id": "c-004",
            "title": "クラウド基礎",
            "status": "準備中",
            "enrolled": 0,
            "completion_rate": 0,
        },
        {
            "id": "c-005",
            "title": "セキュリティ入門",
            "status": "開講中",
            "enrolled": 38,
            "completion_rate": 0.71,
        },
    ]


def _learning_progress() -> List[Dict[str, Any]]:
    return [
        {
            "student_id": "S001",
            "course": "Python基礎",
            "progress": 95,
            "last_accessed": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
        },
        {
            "student_id": "S002",
            "course": "データ分析入門",
            "progress": 60,
            "last_accessed": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        },
        {
            "student_id": "S003",
            "course": "AI/ML実践",
            "progress": 30,
            "last_accessed": (datetime.utcnow() - timedelta(hours=5)).isoformat(),
        },
        {
            "student_id": "S004",
            "course": "Python基礎",
            "progress": 100,
            "last_accessed": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        },
        {
            "student_id": "S005",
            "course": "セキュリティ入門",
            "progress": 45,
            "last_accessed": (datetime.utcnow() - timedelta(hours=12)).isoformat(),
        },
    ]


def _grades() -> List[Dict[str, Any]]:
    return [
        {
            "student_id": "S001",
            "course": "Python基礎",
            "score": 92,
            "grade": "A",
            "submitted_at": (datetime.utcnow() - timedelta(days=3)).isoformat(),
        },
        {
            "student_id": "S002",
            "course": "データ分析入門",
            "score": 78,
            "grade": "B",
            "submitted_at": (datetime.utcnow() - timedelta(days=5)).isoformat(),
        },
        {
            "student_id": "S003",
            "course": "AI/ML実践",
            "score": 65,
            "grade": "C",
            "submitted_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
        },
        {
            "student_id": "S004",
            "course": "Python基礎",
            "score": 98,
            "grade": "A",
            "submitted_at": (datetime.utcnow() - timedelta(days=7)).isoformat(),
        },
        {
            "student_id": "S005",
            "course": "セキュリティ入門",
            "score": 88,
            "grade": "A",
            "submitted_at": (datetime.utcnow() - timedelta(days=2)).isoformat(),
        },
    ]


def _materials() -> List[Dict[str, Any]]:
    return [
        {
            "id": "m-001",
            "title": "Python入門テキスト",
            "type": "PDF",
            "downloads": 320,
            "course": "Python基礎",
        },
        {
            "id": "m-002",
            "title": "データ可視化ハンズオン",
            "type": "Jupyter",
            "downloads": 180,
            "course": "データ分析入門",
        },
        {
            "id": "m-003",
            "title": "モデル学習演習",
            "type": "Jupyter",
            "downloads": 95,
            "course": "AI/ML実践",
        },
        {
            "id": "m-004",
            "title": "AWS入門動画",
            "type": "動画",
            "downloads": 210,
            "course": "クラウド基礎",
        },
    ]


@router.get("/courses")
async def get_courses():
    """コース一覧"""
    return {"items": _courses(), "total": len(_courses())}


@router.get("/learning-progress")
async def get_learning_progress():
    """学習進捗一覧"""
    return {"items": _learning_progress(), "total": len(_learning_progress())}


@router.get("/grades")
async def get_grades():
    """成績一覧"""
    return {"items": _grades(), "total": len(_grades())}


@router.get("/materials")
async def get_materials():
    """教材一覧"""
    return {"items": _materials(), "total": len(_materials())}


@router.get("/dashboard")
async def get_dashboard():
    """ダッシュボードサマリ"""
    courses = _courses()
    return {
        "courses_active": len([c for c in courses if c["status"] == "開講中"]),
        "total_enrolled": sum(c["enrolled"] for c in courses),
        "avg_completion_rate": sum(
            c["completion_rate"] for c in courses if c["completion_rate"] > 0
        )
        / max(1, len([c for c in courses if c["completion_rate"] > 0])),
    }
