"""
人材・組織 モジュール
障害者雇用支援、オンボーディング、スキルマッチング
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


class DisabilitySupportManager:
    """障害者雇用支援"""

    def __init__(self):
        self._supports: Dict[str, Dict[str, Any]] = {}
        self._employees: Dict[str, Dict[str, Any]] = {}

    def register_support(
        self,
        employee_id: str,
        disability_type: str,
        accommodations: List[str],
        disability_grade: Optional[str] = None,
        remote_work_eligible: bool = True,
        notes: Optional[str] = None,
    ) -> Dict[str, Any]:
        """配慮事項を登録"""
        support_id = str(uuid.uuid4())
        support = {
            "id": support_id,
            "employee_id": employee_id,
            "disability_type": disability_type,
            "disability_grade": disability_grade or "",
            "accommodations": accommodations,
            "remote_work_eligible": remote_work_eligible,
            "notes": notes or "",
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._supports[support_id] = support
        return support

    def list_supports(self) -> List[Dict[str, Any]]:
        """登録済み配慮一覧"""
        return list(self._supports.values())

    def get_accommodation_checklist(self) -> List[Dict[str, str]]:
        """合理的配慮チェックリスト"""
        return [
            {"id": "remote", "name": "フルリモート勤務", "category": "勤務形態"},
            {"id": "flex_time", "name": "通院等の時間調整", "category": "勤務形態"},
            {"id": "rest_area", "name": "休憩スペース", "category": "オフィス環境"},
            {"id": "assistive", "name": "補助ツール・機器", "category": "ツール"},
            {"id": "document", "name": "文書のアクセシビリティ対応", "category": "情報アクセス"},
        ]


class OnboardingManager:
    """オンボーディング管理"""

    def __init__(self):
        self._tasks: Dict[str, Dict[str, Any]] = {}
        self._templates: Dict[str, List[Dict[str, Any]]] = {
            "standard": [
                {"task_name": "入社書類提出", "category": "document"},
                {"task_name": "PC・アカウント発行", "category": "equipment"},
                {"task_name": "セキュリティ研修", "category": "training"},
                {"task_name": "システムアクセス権設定", "category": "access"},
            ],
        }

    def create_task(
        self,
        employee_id: str,
        task_name: str,
        category: str,
        due_date: Optional[str] = None,
        assignee_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """オンボーディングタスクを作成"""
        task_id = str(uuid.uuid4())
        task = {
            "id": task_id,
            "employee_id": employee_id,
            "task_name": task_name,
            "category": category,
            "due_date": due_date,
            "assignee_id": assignee_id,
            "status": "pending",
            "completed_at": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
        }
        self._tasks[task_id] = task
        return task

    def create_from_template(
        self, employee_id: str, template: str = "standard"
    ) -> List[Dict[str, Any]]:
        """テンプレートからオンボーディングタスクを一括作成"""
        tasks = []
        for t in self._templates.get(template, []):
            task = self.create_task(
                employee_id=employee_id,
                task_name=t["task_name"],
                category=t["category"],
            )
            tasks.append(task)
        return tasks

    def list_tasks(self, employee_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """タスク一覧"""
        if employee_id:
            return [t for t in self._tasks.values() if t["employee_id"] == employee_id]
        return list(self._tasks.values())

    def complete_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """タスクを完了"""
        if task_id not in self._tasks:
            return None
        task = self._tasks[task_id]
        task["status"] = "completed"
        task["completed_at"] = datetime.utcnow().isoformat()
        task["updated_at"] = datetime.utcnow().isoformat()
        return task


class SkillMatchingManager:
    """スキルマッチング"""

    def __init__(self):
        self._employees: Dict[str, Dict[str, Any]] = {}

    def register_employee_skills(
        self, employee_id: str, skills: List[str], experience_level: str = "mid"
    ) -> Dict[str, Any]:
        """社員スキルを登録"""
        if employee_id not in self._employees:
            self._employees[employee_id] = {
                "employee_id": employee_id,
                "skills": [],
                "experience_level": "mid",
                "created_at": datetime.utcnow().isoformat(),
            }
        emp = self._employees[employee_id]
        emp["skills"] = list(set(emp.get("skills", []) + skills))
        emp["experience_level"] = experience_level
        emp["updated_at"] = datetime.utcnow().isoformat()
        return emp

    def find_matches(
        self,
        required_skills: List[str],
        preferred_skills: Optional[List[str]] = None,
        experience_level: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """スキルマッチング"""
        matches = []
        for emp_id, emp in self._employees.items():
            emp_skills = set(emp.get("skills", []))
            matches_count = sum(1 for s in required_skills if s in emp_skills)
            if matches_count >= len(required_skills) * 0.5:  # 50%以上一致
                score = matches_count / len(required_skills) * 100
                if preferred_skills:
                    preferred_match = sum(
                        1 for s in preferred_skills if s in emp_skills
                    )
                    score += preferred_match * 10
                matches.append(
                    {
                        "employee_id": emp_id,
                        "skills": emp["skills"],
                        "match_score": min(score, 100),
                        "experience_level": emp.get("experience_level", ""),
                    }
                )
        return sorted(matches, key=lambda x: x["match_score"], reverse=True)


disability_support_manager = DisabilitySupportManager()
onboarding_manager = OnboardingManager()
skill_matching_manager = SkillMatchingManager()
