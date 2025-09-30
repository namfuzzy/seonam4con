from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.site import Site
    from app.models.page_metric import PageMetric
    from app.models.cwv_metric import CWVMetric
    from app.models.internal_link import InternalLink
    from app.models.content import ContentDraft
    from app.models.links import LinkScore


class PageStatus(str):
    DRAFT = "draft"
    PUBLISHED = "published"


class Page(TimestampMixin, Base):
    __tablename__ = "pages"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"))
    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    title: Mapped[Optional[str]] = mapped_column(String(255))
    status: Mapped[Optional[str]] = mapped_column(String(32), default=PageStatus.PUBLISHED)
    last_crawled_at: Mapped[Optional[str]] = mapped_column(String(64))

    site: Mapped["Site"] = relationship(back_populates="pages")
    metrics: Mapped[List["PageMetric"]] = relationship(back_populates="page", cascade="all, delete-orphan")
    cwv_metrics: Mapped[List["CWVMetric"]] = relationship(back_populates="page", cascade="all, delete-orphan")
    incoming_links: Mapped[List["InternalLink"]] = relationship(
        back_populates="to_page", foreign_keys="InternalLink.to_page_id", cascade="all, delete-orphan"
    )
    outgoing_links: Mapped[List["InternalLink"]] = relationship(
        back_populates="from_page", foreign_keys="InternalLink.from_page_id", cascade="all, delete-orphan"
    )
