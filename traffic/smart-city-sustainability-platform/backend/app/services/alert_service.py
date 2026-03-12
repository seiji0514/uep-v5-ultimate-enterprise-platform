"""
アラートサービス
"""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.alert import Alert
from loguru import logger


class AlertService:
    """アラートサービス"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_alerts(
        self,
        sensor_id: Optional[str] = None,
        alert_type: Optional[str] = None,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """アラート一覧の取得"""
        query = self.db.query(Alert)
        
        if sensor_id:
            query = query.filter(Alert.sensor_id == sensor_id)
        if alert_type:
            query = query.filter(Alert.alert_type == alert_type)
        if severity:
            query = query.filter(Alert.severity == severity)
        if status:
            query = query.filter(Alert.status == status)
        
        alerts = query.offset(skip).limit(limit).all()
        return [{
            "id": str(alert.id),
            "sensor_id": str(alert.sensor_id),
            "alert_type": alert.alert_type,
            "severity": alert.severity,
            "message": alert.message,
            "status": alert.status,
            "created_at": alert.created_at.isoformat()
        } for alert in alerts]
    
    def acknowledge_alert(self, alert_id: str, user_id: str) -> bool:
        """アラートの承認"""
        try:
            alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                return False
            
            alert.status = "acknowledged"
            alert.acknowledged_by = user_id
            alert.acknowledged_at = datetime.now()
            
            self.db.commit()
            logger.info(f"アラート承認成功: alert_id={alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"アラート承認エラー: {e}")
            raise
    
    def resolve_alert(self, alert_id: str) -> bool:
        """アラートの解決"""
        try:
            alert = self.db.query(Alert).filter(Alert.id == alert_id).first()
            if not alert:
                return False
            
            alert.status = "resolved"
            alert.resolved_at = datetime.now()
            
            self.db.commit()
            logger.info(f"アラート解決成功: alert_id={alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"アラート解決エラー: {e}")
            raise

