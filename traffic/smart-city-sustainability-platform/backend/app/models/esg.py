"""
ESGモデル
"""

from sqlalchemy import Column, String, Date, JSON, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.core.database import Base


class ESGReport(Base):
    """ESGレポートテーブル"""
    __tablename__ = "esg_reports"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    report_name = Column(String(255), nullable=False)
    report_type = Column(String(50), nullable=False)  # environment, social, governance, integrated
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    status = Column(String(50), default="draft")  # draft, generated, published
    file_path = Column(String(500))
    metadata = Column(JSON)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class CarbonFootprint(Base):
    """カーボンフットプリントテーブル"""
    __tablename__ = "carbon_footprint"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    scope = Column(String(50), nullable=False)  # scope1, scope2, scope3
    category = Column(String(100))
    value = Column(Float, nullable=False)
    unit = Column(String(50), default="tCO2e")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

