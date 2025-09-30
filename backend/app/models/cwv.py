from datetime import date

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, JSON
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CWVMetric(Base):
    __tablename__ = "cwv_metrics"

    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    date = Column(Date, default=date.today)
    lcp = Column(Float, nullable=True)
    inp = Column(Float, nullable=True)
    cls = Column(Float, nullable=True)
    lab_json = Column(JSON, nullable=True)
    field_json = Column(JSON, nullable=True)

    page = relationship("Page", back_populates="cwv_metrics")
