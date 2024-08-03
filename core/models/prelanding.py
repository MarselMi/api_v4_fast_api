from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, ForeignKey
from core.models import Base

import enum

if TYPE_CHECKING:
    from .partner import Partner
    from .offer import Offer


class StatusChoices(enum.Enum):
    ACTIVE = "Активный"
    DISABLE = "Отключен"
    DELETE = "Удален"


class TypeChoices(enum.Enum):
    PUBLIC = "Публичный"
    PRIVATE = "Приватный"


class Prelanding(Base):
    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"),
        server_default=None,
        default=None,
        nullable=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    screenshot: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(15),
        Enum(StatusChoices),
        default=StatusChoices.ACTIVE.value,
        server_default=StatusChoices.ACTIVE.value,
    )
    type: Mapped[str] = mapped_column(
        String(15),
        Enum(TypeChoices),
        default=TypeChoices.PUBLIC.value,
        server_default=TypeChoices.PUBLIC.value,
    )
    private_partners: Mapped[list["Partner"] | None] = relationship(
        back_populates="prelandings_private",
        secondary="partners_of_the_prelandings_association",
    )
    # offer: Mapped["Offer"] = relationship(
    #     back_populates="prelandings",
    # )
