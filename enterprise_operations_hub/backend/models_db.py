"""SQLAlchemy モデル"""
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text

from database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(128))
    hashed_password = Column(String(256), nullable=False)
    full_name = Column(String(128))
    role = Column(String(32), default="viewer")  # admin, operator, viewer
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class Observation(Base):
    __tablename__ = "observations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(64), default="default", index=True)
    domain = Column(String(64), default="general", index=True)
    type = Column(String(64), default="")
    title = Column(String(256), nullable=False)
    severity = Column(String(32), default="中")
    status = Column(String(32), default="要対応")
    created_at = Column(DateTime, default=datetime.utcnow)


class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(64), default="default", index=True)
    domain = Column(String(64), default="general", index=True)
    escalation_level = Column(Integer, default=0)  # 0=通常, 1=エスカレーション中
    approved_by = Column(String(128), default="")
    title = Column(String(256), nullable=False)
    assignee = Column(String(128), default="")
    due_date = Column(String(32), default="")
    status = Column(String(32), default="未着手")
    created_at = Column(DateTime, default=datetime.utcnow)


class Risk(Base):
    __tablename__ = "risks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(64), default="default", index=True)
    domain = Column(String(64), default="general", index=True)
    type = Column(String(64), default="")
    title = Column(String(256), nullable=False)
    level = Column(String(32), default="中")
    status = Column(String(32), default="監視中")
    created_at = Column(DateTime, default=datetime.utcnow)


class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    domain = Column(String(64), default="general")
    type = Column(String(64), default="")  # threshold, deadline, anomaly
    title = Column(String(256), nullable=False)
    message = Column(Text, default="")
    severity = Column(String(32), default="中")  # 低, 中, 高, 緊急
    read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(String(64), default="default", index=True)
    user_id = Column(String(64), default="")
    action = Column(String(64), nullable=False)  # create, update, delete, export
    resource_type = Column(String(64), default="")  # observation, task, risk, alert
    resource_id = Column(String(64), default="")
    details = Column(Text, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
