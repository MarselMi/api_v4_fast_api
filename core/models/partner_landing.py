from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from core.models import Base

if TYPE_CHECKING:
    from .partner import Partner


class PartnerLanding(Base):
    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"),
        nullable=True
    )

    landings: Mapped[list["Partner"] | None] = relationship(
        back_populates="partner_landings",
        secondary="landing_of_the_partner_association",
    )
