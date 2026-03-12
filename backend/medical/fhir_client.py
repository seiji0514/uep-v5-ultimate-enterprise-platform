"""
FHIR クライアント
HL7 FHIR 連携、HIPAA 準拠
補強スキル: 医療、FHIR
"""
import os
from typing import Any, Dict, List, Optional

# fhirclient はオプショナル: pip install fhirclient
try:
    from fhirclient import client
    from fhirclient.models.fhirdate import FHIRDate

    FHIR_AVAILABLE = True
except ImportError:
    FHIR_AVAILABLE = False
    client = None


class FHIRClient:
    """FHIR クライアント（スケルトン）"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        app_id: Optional[str] = None,
    ):
        self.base_url = base_url or os.getenv(
            "FHIR_SERVER_URL", "http://localhost:8080/fhir"
        )
        self.app_id = app_id or os.getenv("FHIR_APP_ID", "uep-medical")
        self._client = None

    def _get_client(self):
        if not FHIR_AVAILABLE:
            raise RuntimeError("fhirclient not installed. pip install fhirclient")
        if self._client is None:
            settings = client.FHIRClientSettings(
                url=self.base_url,
                app_id=self.app_id,
            )
            self._client = client.FHIRClient(settings=settings)
        return self._client

    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """患者リソースを取得（デモ）"""
        if not FHIR_AVAILABLE:
            return {"resourceType": "Patient", "id": patient_id, "demo": True}
        try:
            c = self._get_client()
            patient = c.read("Patient", patient_id)
            return patient.as_json() if patient else None
        except Exception:
            return None

    def search_observations(
        self,
        patient_id: str,
        code: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Observation を検索（デモ）"""
        if not FHIR_AVAILABLE:
            return [
                {"resourceType": "Observation", "subject": patient_id, "demo": True}
            ]
        try:
            c = self._get_client()
            search = c.resource("Observation").search(patient=patient_id)
            return [r.as_json() for r in search]
        except Exception:
            return []


fhir_client = FHIRClient()
