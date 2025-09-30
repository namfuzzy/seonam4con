from typing import List, Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.site import Site
    from app.models.user import User
    from app.models.log import AuditLog
    from app.models.alert import Alert


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    goals: Mapped[Optional[str]] = mapped_column(Text, default=None)

    owner: Mapped["User"] = relationship(back_populates="projects")
    sites: Mapped[List["Site"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    alerts: Mapped[List["Alert"]] = relationship(back_populates="project", cascade="all, delete-orphan")
    logs: Mapped[List["AuditLog"]] = relationship(back_populates="project", cascade="all, delete-orphan")
