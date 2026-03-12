"""
判断支援モデル
"""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class DecisionSupportLog(Base):
    """判断支援ログテーブル"""
    __tablename__ = "decision_support_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    decision_type = Column(String(100), nullable=False)
    scenario_analysis = Column(JSON)
    risk_assessment = Column(JSON)
    decision_recommendation = Column(Text)
    decision_made = Column(Text)
    created_at = Column(DateTime, server_default=func.now())


class Runbook(Base):
    """Runbookテーブル"""
    __tablename__ = "runbooks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    runbook_name = Column(String(255), nullable=False)
    runbook_type = Column(String(50), nullable=False)  # environment_management, smart_city_management, disaster_response
    content = Column(Text, nullable=False)
    status = Column(String(50), default="draft")  # draft, active, archived
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

