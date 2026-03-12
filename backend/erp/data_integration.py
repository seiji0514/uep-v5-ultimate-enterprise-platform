"""
ERP - データ連携基盤
基幹システムと周辺システムの連携・データ統合
"""
from datetime import datetime
from typing import Any, Dict, List, Optional


class DataIntegrationManager:
    """データ連携オーケストレーター"""
    _rules: Dict[str, Dict[str, Any]]
    _sync_logs: List[Dict[str, Any]]

    def __init__(self):
        self._rules = {}
        self._sync_logs = []

    def create_rule(self, source: str, target: str, sync_type: str, schedule: Optional[str] = None, mapping: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        rule_id = f"sync-{source}-{target}"
        rule = {
            "id": rule_id,
            "source_system": source,
            "target_system": target,
            "sync_type": sync_type,
            "schedule": schedule,
            "mapping": mapping or {},
            "enabled": True,
            "created_at": datetime.utcnow().isoformat(),
        }
        self._rules[rule_id] = rule
        return rule

    def list_rules(self) -> List[Dict[str, Any]]:
        return list(self._rules.values())

    def get_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        return self._rules.get(rule_id)

    def execute_sync(self, rule_id: str) -> Dict[str, Any]:
        rule = self._rules.get(rule_id)
        if not rule:
            return {"success": False, "error": "Rule not found"}
        log = {
            "rule_id": rule_id,
            "executed_at": datetime.utcnow().isoformat(),
            "status": "success",
            "records_synced": 0,
        }
        self._sync_logs.append(log)
        return {"success": True, "log": log}

    def get_sync_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        return sorted(self._sync_logs, key=lambda x: x["executed_at"], reverse=True)[:limit]

    def get_summary(self) -> Dict[str, Any]:
        return {
            "rules_count": len(self._rules),
            "last_sync_count": len(self._sync_logs),
            "systems": ["erp_sales", "erp_purchasing", "accounting", "hr", "unified_business"],
        }


data_integration_manager = DataIntegrationManager()
