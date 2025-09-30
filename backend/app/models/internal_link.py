from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class InternalLink(Base):
    __tablename__ = "internal_links"

    id: Mapped[int] = mapped_column(primary_key=True)
    from_page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"))
    to_page_id: Mapped[int] = mapped_column(ForeignKey("pages.id", ondelete="CASCADE"))
    anchor_text: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[float] = mapped_column(Float, default=0.0)

    from_page = relationship("Page", foreign_keys=[from_page_id], back_populates="outgoing_links")
    to_page = relationship("Page", foreign_keys=[to_page_id], back_populates="incoming_links")
