from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.project import Project
    from app.models.integration import Integration
    from app.models.gsc import GscSite
    from app.models.page import Page


class Site(TimestampMixin, Base):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    domain: Mapped[str] = mapped_column(String(255), nullable=False)
    wp_base_url: Mapped[Optional[str]] = mapped_column(String(255), default=None)

    project: Mapped["Project"] = relationship(back_populates="sites")
    integrations: Mapped[List["Integration"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    gsc_sites: Mapped[List["GscSite"]] = relationship(back_populates="site", cascade="all, delete-orphan")
    pages: Mapped[List["Page"]] = relationship(back_populates="site", cascade="all, delete-orphan")
