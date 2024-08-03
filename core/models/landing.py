from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, ForeignKey
from core.models import Base, Partner

import enum

if TYPE_CHECKING:
    from .partner import Partner
    from .landing_element import LandingElement
    from .offer import Offer


class StatusChoices(enum.Enum):
    ACTIVE = "Активный"
    DISABLE = "Отключен"
    DELETE = "Удален"


class TypeChoices(enum.Enum):
    PUBLIC = "Публичный"
    PRIVATE = "Приватный"


class Landing(Base):
    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    screenshot: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(100),
        Enum(StatusChoices),
        default=StatusChoices.ACTIVE.value,
        server_default=StatusChoices.ACTIVE.value,
    )
    type: Mapped[str] = mapped_column(
        String(100),
        Enum(TypeChoices),
        default=TypeChoices.PUBLIC.value,
        server_default=TypeChoices.PUBLIC.value,
    )
    landing_elements: Mapped[int | None] = mapped_column(
        ForeignKey("landingelements.id", ondelete="SET NULL"),
        nullable=True,
    )
    # land_elements: Mapped["LandingElement"] = relationship(
    #     back_populates="landing",
    # )

    private_partners: Mapped[list["Partner"] | None] = relationship(
        back_populates="landings_private",
        secondary="partners_of_the_landings_association",
    )

    # offer: Mapped["Offer"] = relationship(back_populates="landings")
