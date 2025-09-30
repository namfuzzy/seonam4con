from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class IntegrationType(str, PyEnum):
    GSC = "gsc"
    PSI = "psi"
    WORDPRESS = "wordpress"
    INDEXNOW = "indexnow"
    GEMINI = "gemini"


class Integration(Base):
    __tablename__ = "integrations"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    type = Column(Enum(IntegrationType), nullable=False)
    enabled = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", backref="integrations")
    credentials = relationship("Credential", back_populates="integration", cascade="all, delete-orphan")


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True, index=True)
    integration_id = Column(Integer, ForeignKey("integrations.id"), nullable=False)
    key_name = Column(String, nullable=False)
    value_encrypted = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    integration = relationship("Integration", back_populates="credentials")
