from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.log import AuditLog


class UserRole(str):
    ADMIN = "admin"
    OWNER = "owner"
    EDITOR = "editor"
    WRITER = "writer"
    VIEWER = "viewer"


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(32), default=UserRole.OWNER)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    projects: Mapped[List["Project"]] = relationship(back_populates="owner")
    logs: Mapped[List["AuditLog"]] = relationship(back_populates="user")
