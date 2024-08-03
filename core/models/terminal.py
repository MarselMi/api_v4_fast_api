from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Enum, text, ForeignKey
from core.models import Base

import enum


class CurrencyChoices(enum.Enum):
    RUR = "RUR"
    USD = "USD"
    EUR = "EUR"


class Terminal(Base):
    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"),
        server_default=None,
        default=None,
        nullable=True,
    )
    paysystem_id: Mapped[int | None] = mapped_column(
        ForeignKey("paysystems.id", ondelete="SET NULL"), nullable=True
    )

    organisation_id: Mapped[int | None] = mapped_column(
        ForeignKey("organisations.id", ondelete="SET NULL"), nullable=True
    )

    kassa_id: Mapped[int | None] = mapped_column(
        ForeignKey("kassas.id", ondelete="SET NULL"), nullable=True
    )

    acqu_bank: Mapped[int | None] = mapped_column(
        ForeignKey("acqubanks.id", ondelete="SET NULL"), nullable=True
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)

    paysystem_service_id: Mapped[str] = mapped_column(String(500), nullable=False)

    paysystem_public_id: Mapped[str] = mapped_column(String(500), nullable=False)

    paysystem_secret_key: Mapped[str] = mapped_column(String(500), nullable=False)

    one_time_pay: Mapped[int] = mapped_column(default=0, server_default=text("0"))

    contains_rebills: Mapped[int] = mapped_column(default=0, server_default=text("0"))

    rebills: Mapped[int] = mapped_column(default=0, server_default=text("0"))

    paysystem_service_name: Mapped[str | None] = mapped_column(Text, nullable=True)

    status: Mapped[str | None] = mapped_column(Text, nullable=True)

    percent: Mapped[int | None] = mapped_column(
        default=0, server_default=text("0"), nullable=True
    )

    selected: Mapped[int | None] = mapped_column(
        default=0, server_default=text("0"), nullable=True
    )

    rebill_terminal_id: Mapped[int | None] = mapped_column(
        default=0, server_default=text("0"), nullable=True
    )

    currency: Mapped[str] = mapped_column(
        String(10),
        Enum(CurrencyChoices),
        default=CurrencyChoices.RUR.value,
        server_default=CurrencyChoices.RUR.value,
    )
