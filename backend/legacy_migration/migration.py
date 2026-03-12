"""
レガシー移行ツール
データ移行・検証
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional


class LegacyMigrationManager:
    """レガシー移行マネージャー"""
    _jobs: Dict[str, Dict[str, Any]]
    _validation_results: List[Dict[str, Any]]

    def __init__(self):
        self._jobs = {}
        self._validation_results = []

    def create_job(self, source_type: str, source_config: Dict[str, Any], target_system: str, mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        job_id = f"mig-{uuid.uuid4().hex[:12]}"
        job = {
            "id": job_id,
            "source_type": source_type,
            "source_config": source_config,
            "target_system": target_system,
            "mapping": mapping or {},
            "status": "created",
            "records_imported": 0,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Dict[str, Any]]:
        return self._jobs.get(job_id)

    def list_jobs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return sorted(self._jobs.values(), key=lambda x: x["created_at"], reverse=True)[:limit]

    def run_migration(self, job_id: str) -> Dict[str, Any]:
        job = self._jobs.get(job_id)
        if not job:
            return {"success": False, "error": "Job not found"}
        job["status"] = "completed"
        job["records_imported"] = 0  # デモ用
        job["completed_at"] = datetime.utcnow().isoformat()
        return {"success": True, "job": job}

    def validate_migration(self, job_id: str, compare_field: str) -> Dict[str, Any]:
        job = self._jobs.get(job_id)
        if not job:
            return {"success": False, "error": "Job not found"}
        result = {
            "job_id": job_id,
            "compare_field": compare_field,
            "source_count": 0,
            "target_count": 0,
            "match": True,
            "validated_at": datetime.utcnow().isoformat(),
        }
        self._validation_results.append(result)
        return {"success": True, "validation": result}

    def get_summary(self) -> Dict[str, Any]:
        return {
            "jobs_count": len(self._jobs),
            "validations_count": len(self._validation_results),
            "supported_sources": ["csv", "excel", "db", "api"],
            "supported_targets": ["erp_sales", "erp_purchasing", "accounting"],
        }


legacy_migration_manager = LegacyMigrationManager()
