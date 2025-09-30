from datetime import date, datetime

from sqlalchemy import Column, Date, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class GSCSite(Base):
    __tablename__ = "gsc_sites"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    property_uri = Column(String, nullable=False)

    site = relationship("Site", backref="gsc_sites")


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    url = Column(String, nullable=False, index=True)
    title = Column(String, nullable=True)
    status = Column(String, nullable=True)
    last_crawled_at = Column(DateTime, nullable=True)

    site = relationship("Site", back_populates="pages")
    metrics = relationship("PageMetric", back_populates="page")
    cwv_metrics = relationship("CWVMetric", back_populates="page")


class Query(Base):
    __tablename__ = "queries"

    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(Integer, ForeignKey("sites.id"), nullable=False)
    query_text = Column(String, nullable=False)


class PageMetric(Base):
    __tablename__ = "page_metrics"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    date = Column(Date, default=date.today)
    clicks = Column(Float, default=0)
    impressions = Column(Float, default=0)
    ctr = Column(Float, default=0)
    position = Column(Float, default=0)

    page = relationship("Page", back_populates="metrics")
