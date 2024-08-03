from typing import TYPE_CHECKING

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, text, Text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum

if TYPE_CHECKING:
    from .partner import Partner
    from .manager import Manager
    from .transaction import Transaction
    from .chargeback import Chargeback
    from .payout_requisite import PayoutRequisite


class TypeChoices(enum.Enum):
    PAYMENT_REQUEST = "Заявка на выплату"
    FINE = "Штраф"
    CORRECTION = "Коррекция"
    COMPENSATION = "Компенсация"


class StatusChoices(enum.Enum):
    IN_PROCESS = "В обработке"
    PROCESSED = "Выполнено"
    CANCELLED = "Отменена"


class CurrencyChoices(enum.Enum):
    RUR = "RUR"
    USD = "USD"
    EUR = "EUR"


class Payout(Base):
    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"), nullable=True
    )

    # partners: Mapped["Partner"] = relationship(
    #     back_populates="partners"
    # )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"), nullable=True
    )

    # managers: Mapped["Manager"] = relationship(
    #     back_populates="managers"
    # )

    chargeback_id: Mapped[int | None] = mapped_column(
        ForeignKey("chargebacks.id", ondelete="SET NULL"), nullable=True
    )
    #
    # chargebacks: Mapped["Chargeback"] = relationship(
    #     back_populates="chargebacks"
    # )

    request_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    request_date_day: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
        nullable=True,
    )

    request_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
        nullable=True,
    )

    type: Mapped[str | None] = mapped_column(
        String(50),
        Enum(TypeChoices),
        server_default=TypeChoices.PAYMENT_REQUEST.value,
        default=TypeChoices.PAYMENT_REQUEST.value,
    )

    status: Mapped[str | None] = mapped_column(
        String(50),
        Enum(StatusChoices),
        server_default=StatusChoices.IN_PROCESS.value,
        default=StatusChoices.IN_PROCESS.value,
    )

    payment_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=None,
        nullable=True,
    )

    payment_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    payment_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
    )

    sum: Mapped[float] = mapped_column(nullable=False)

    comission: Mapped[float | None] = mapped_column(nullable=True)

    requisites_id: Mapped[int | None] = mapped_column(
        ForeignKey("payoutrequisites.id", ondelete="SET NULL"), nullable=True
    )

    # payoutrequisites: Mapped["PayoutRequisite"] = relationship(
    #     back_populates="payoutrequisites"
    # )

    requisites: Mapped[str] = mapped_column(Text, nullable=False)

    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id", ondelete="SET NULL"), nullable=True
    )

    # transactions: Mapped["Transaction"] = relationship(
    #     back_populates="transactions"
    # )

    selected_requisites: Mapped[str] = mapped_column(
        String(250), default="-", server_default="-", nullable=False
    )

    fix: Mapped[float] = mapped_column(
        default=0.0, server_default=text("0.0"), nullable=False
    )

    comment: Mapped[str] = mapped_column(Text, nullable=True)

    payment_sum: Mapped[float | None] = mapped_column(nullable=True)

    processed: Mapped[int] = mapped_column(
        default=1, server_default=text("1"), nullable=False
    )

    currency: Mapped[str | None] = mapped_column(
        String(10),
        Enum(CurrencyChoices),
        server_default=CurrencyChoices.RUR.value,
        default=CurrencyChoices.RUR.value,
    )

    batch_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
