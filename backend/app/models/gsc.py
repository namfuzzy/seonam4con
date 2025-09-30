from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.site import Site


class GscSite(TimestampMixin, Base):
    __tablename__ = "gsc_sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id", ondelete="CASCADE"))
    property_uri: Mapped[str] = mapped_column(String(255), nullable=False)

    site: Mapped["Site"] = relationship(back_populates="gsc_sites")
