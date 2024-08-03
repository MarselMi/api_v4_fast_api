from typing import TYPE_CHECKING

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum

if TYPE_CHECKING:
    from .transaction import Transaction
    from .incoming_transaction import IncomingTransaction
    from .partner import Partner


class TypeChoices(enum.Enum):
    bank = "bank"
    operator = "operator"


class CurrencyChoices(enum.Enum):
    RUR = "RUR"
    USD = "USD"
    EUR = "EUR"


class Chargeback(Base):
    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("transactions.id", ondelete="SET NULL"),
        nullable=True
    )

    transactions: Mapped["Transaction"] = relationship(
        back_populates="transactions"
    )

    intransaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("incomingtransactions.id", ondelete="SET NULL"),
        nullable=True
    )

    incomingtransactions: Mapped["IncomingTransaction"] = relationship(
        back_populates="incomingtransactions"
    )

    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"),
        nullable=True
    )

    partners: Mapped["Partner"] = relationship(
        back_populates="partners"
    )

    n_client_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_offer_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_host_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_stream_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_terminal_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    sum: Mapped[float | None] = mapped_column(
        nullable=True
    )

    type: Mapped[str | None] = mapped_column(
        String(50),
        Enum(TypeChoices),
        server_default=TypeChoices.bank.value,
        default=TypeChoices.bank.value,
    )

    create_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    create_date_day: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
        nullable=True,
    )

    create_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
        nullable=True,
    )

    currency: Mapped[str | None] = mapped_column(
        String(10),
        Enum(CurrencyChoices),
        server_default=CurrencyChoices.RUR.value,
        default=CurrencyChoices.RUR.value,
    )
