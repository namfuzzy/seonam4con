from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Float, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base

if TYPE_CHECKING:
    from app.models.page import Page


class CWVMetric(Base):
    __tablename__ = "cwv_metrics"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"))
    date: Mapped[date] = mapped_column(Date, nullable=False)
    lcp: Mapped[Optional[float]] = mapped_column(Float, default=None)
    inp: Mapped[Optional[float]] = mapped_column(Float, default=None)
    cls: Mapped[Optional[float]] = mapped_column(Float, default=None)
    lab_json: Mapped[Optional[dict]] = mapped_column(JSON, default=None)
    field_json: Mapped[Optional[dict]] = mapped_column(JSON, default=None)

    page: Mapped["Page"] = relationship(back_populates="cwv_metrics")
