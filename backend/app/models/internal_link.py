from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String

from app.db.base_class import Base


class InternalLink(Base):
    __tablename__ = "internal_links"

    id = Column(Integer, primary_key=True, index=True)
    from_page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    to_page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    anchor_text = Column(String, nullable=False)
    score = Column(Float, default=0)


class LinkScore(Base):
    __tablename__ = "linkscore"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    date = Column(Date, default=date.today)
    score = Column(Float, default=0)
