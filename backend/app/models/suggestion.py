from datetime import datetime
from enum import Enum as PyEnum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, JSON

from app.db.base_class import Base


class SuggestionType(str, PyEnum):
    ONPAGE = "onpage"
    INTERNAL = "internal"
    TECH = "tech"


class Suggestion(Base):
    __tablename__ = "suggestions"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    type = Column(Enum(SuggestionType), nullable=False)
    payload_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
