from enum import Enum
from typing import TYPE_CHECKING, List

from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin


class IntegrationType(str, Enum):
    GSC = "GSC"
    PSI = "PSI"
    WORDPRESS = "WP"
    INDEXNOW = "INDEXNOW"
    GEMINI = "GEMINI"


if TYPE_CHECKING:
    from app.models.site import Site
    from app.models.credential import Credential


class Integration(TimestampMixin, Base):
    __tablename__ = "integrations"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"))
    type: Mapped[str] = mapped_column(String(32))
    enabled: Mapped[bool] = mapped_column(Boolean, default=False)

    site: Mapped["Site"] = relationship(back_populates="integrations")
    credentials: Mapped[List["Credential"]] = relationship(
        back_populates="integration", cascade="all, delete-orphan"
    )
