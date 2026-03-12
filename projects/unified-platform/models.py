"""Phase 1: SQLAlchemy Models - Medical, Aviation, Space"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    """認証ユーザー - 複数ユーザー・パスワードハッシュ"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(32), default="user")  # admin, user
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Notification(Base):
    """通知センター - アラート一覧・既読管理"""
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128), nullable=False)
    body = Column(Text, nullable=True)
    severity = Column(String(16), default="info")  # info, warning, error, success
    domain = Column(String(32), nullable=True)  # medical, aviation, space
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Phase 2: Audit Log - Compliance"""
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String(64), nullable=True)
    action = Column(String(64), nullable=False)
    resource = Column(String(128), nullable=False)
    resource_id = Column(String(64), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)


# --- Medical ---
class Patient(Base):
    __tablename__ = "patients"
    id = Column(String(32), primary_key=True)
    identifier = Column(String(64), unique=True)
    family_name = Column(String(128))
    given_name = Column(String(128))
    gender = Column(String(16))
    birth_date = Column(String(16))
    created_at = Column(DateTime, default=datetime.utcnow)


class AIDiagnosis(Base):
    __tablename__ = "ai_diagnoses"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(32), ForeignKey("patients.id"))
    finding = Column(String(256))
    confidence = Column(Float)
    status = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)


class VitalSign(Base):
    __tablename__ = "vital_signs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(String(32), ForeignKey("patients.id"))
    heart_rate = Column(Integer)
    blood_pressure = Column(String(32))
    spo2 = Column(Integer)
    recorded_at = Column(DateTime, default=datetime.utcnow)


# --- Aviation ---
class Flight(Base):
    __tablename__ = "flights"
    id = Column(Integer, primary_key=True, autoincrement=True)
    flight_id = Column(String(32), unique=True)
    route = Column(String(32))
    departure = Column(String(16))
    arrival = Column(String(16))
    status = Column(String(64))
    aircraft = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)


class Airport(Base):
    __tablename__ = "airports"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(8), unique=True)
    departures_today = Column(Integer, default=0)
    arrivals_today = Column(Integer, default=0)
    congestion = Column(String(16))
    weather = Column(String(64))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# --- Space ---
class Satellite(Base):
    __tablename__ = "satellites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    satellite_id = Column(String(64), unique=True)
    name = Column(String(128))
    orbit_km = Column(Float)
    inclination = Column(Float)
    period_min = Column(Float)
    status = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)


class Launch(Base):
    __tablename__ = "launches"
    id = Column(Integer, primary_key=True, autoincrement=True)
    launch_id = Column(String(32), unique=True)
    mission = Column(String(128))
    launch_date = Column(String(16))
    vehicle = Column(String(64))
    status = Column(String(32))
    created_at = Column(DateTime, default=datetime.utcnow)
