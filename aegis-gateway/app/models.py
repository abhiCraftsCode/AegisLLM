import uuid
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Integer, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    api_keys: Mapped[List["APIKey"]] = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")


class APIKey(Base):
    __tablename__ = "api_keys"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)  # e.g. "E-commerce Bot Key"
    key_prefix: Mapped[str] = mapped_column(String(12), nullable=False) # e.g. "aegis_sec_a1b2" for UI display
    key_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False) # SHA-256 Hash
    
    rate_limit_rpm: Mapped[int] = mapped_column(Integer, default=60) # Requests Per Minute limit
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="api_keys")
    audit_logs: Mapped[List["AuditLog"]] = relationship("AuditLog", back_populates="api_key", cascade="all, delete-orphan")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    api_key_id: Mapped[str] = mapped_column(String, ForeignKey("api_keys.id"), nullable=False, index=True)
    
    # Privacy-Safe Audit Metrics (Zero Full Raw Text)
    prompt_hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    prompt_preview: Mapped[str] = mapped_column(String(40), nullable=False) # Max 40-character safe snippet
    
    action: Mapped[str] = mapped_column(String(20), nullable=False) # "ALLOWED" or "BLOCKED"
    tier_triggered: Mapped[Optional[str]] = mapped_column(String(50), nullable=True) # "TIER_1_HEURISTIC" or "TIER_2_DEBERTA_ONNX"
    threat_score: Mapped[float] = mapped_column(Float, default=0.0)
    latency_ms: Mapped[float] = mapped_column(Float, nullable=False)
    
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    api_key: Mapped["APIKey"] = relationship("APIKey", back_populates="audit_logs")