from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String, Text

from app.db.base_class import Base


class ContentBrief(Base):
    __tablename__ = "content_briefs"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    topic = Column(String, nullable=False)
    intent = Column(String, nullable=True)
    stage = Column(String, nullable=True)
    outline_json = Column(JSON, nullable=True)
    checklist_json = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentDraft(Base):
    __tablename__ = "content_drafts"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    wp_post_id = Column(Integer, nullable=True)
    title = Column(String, nullable=False)
    slug = Column(String, nullable=True)
    html = Column(Text, nullable=True)
    schema_json = Column(JSON, nullable=True)
    score_onpage = Column(Float, nullable=True)
    status = Column(String, default="draft")
    created_at = Column(DateTime, default=datetime.utcnow)
