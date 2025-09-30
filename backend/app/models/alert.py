from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class AlertSeverity(str):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Alert(TimestampMixin, Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    severity: Mapped[str] = mapped_column(String(16), default=AlertSeverity.LOW)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    detail: Mapped[str | None] = mapped_column(Text, default=None)

    project = relationship("Project", back_populates="alerts")
