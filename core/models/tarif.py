from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text, ForeignKey, Enum
from core.models import Base

import enum

if TYPE_CHECKING:
    from .offer import Offer


class TypeChoices(enum.Enum):
    standart = "Стандартный"
    lower = "Пониженный"
    higher = "Повышенный"


class CurrencyChoices(enum.Enum):
    RUR = "RUR"
    USD = "USD"
    EUR = "EUR"


class Tarif(Base):
    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"),
        nullable=True
    )

    offers: Mapped["Offer"] = relationship(
        back_populates="offers"
    )

    type: Mapped[str | None] = mapped_column(
        String(50),
        Enum(TypeChoices),
        server_default=TypeChoices.standart.value,
        default=TypeChoices.standart.value,
    )

    tarif_name: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    freeday: Mapped[int | None] = mapped_column(
        nullable=True
    )

    freeday_sum: Mapped[float | None] = mapped_column(
        nullable=True
    )

    tarif_sum: Mapped[float | None] = mapped_column(
        nullable=True
    )

    period: Mapped[int | None] = mapped_column(
        nullable=True
    )

    two_tarif_name: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    two_tarif_sum: Mapped[float | None] = mapped_column(
        nullable=True
    )

    two_period: Mapped[int | None] = mapped_column(
        nullable=True
    )

    selected: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
        server_default=text("0")
    )

    currency: Mapped[str | None] = mapped_column(
        String(10),
        Enum(CurrencyChoices),
        server_default=CurrencyChoices.RUR.value,
        default=CurrencyChoices.RUR.value,
    )
