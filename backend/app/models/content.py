from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


if TYPE_CHECKING:
    from app.models.page import Page
    from app.models.site import Site


class ContentBrief(TimestampMixin, Base):
    __tablename__ = "content_briefs"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"))
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    intent: Mapped[str] = mapped_column(String(32), nullable=False)
    stage: Mapped[str] = mapped_column(String(32), nullable=False)
    outline_json: Mapped[dict] = mapped_column(JSON, default=dict)
    checklist_json: Mapped[dict] = mapped_column(JSON, default=dict)

    site = relationship("Site")


class ContentDraft(TimestampMixin, Base):
    __tablename__ = "content_drafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"))
    wp_post_id: Mapped[int | None] = mapped_column(ForeignKey("pages.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255))
    html: Mapped[str] = mapped_column(Text)
    schema_json: Mapped[dict | None] = mapped_column(JSON, default=None)
    score_onpage: Mapped[float | None] = mapped_column(Float, default=None)
    status: Mapped[str] = mapped_column(String(32), default="draft")

    site = relationship("Site")
    wp_page = relationship("Page", foreign_keys=[wp_post_id])
