import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum


class LabelChoices(enum.Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    REBILL = "REBILL"
    REFUND = "REFUND"


class Check(Base):
    client_id: Mapped[int | None] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True
    )

    incoming_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("incomingtransactions.id", ondelete="SET NULL"),
        nullable=True
    )

    type: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    label: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    price: Mapped[float | None] = mapped_column(
        nullable=True
    )

    quantity: Mapped[float | None] = mapped_column(
        nullable=True
    )

    amount: Mapped[float | None] = mapped_column(
        nullable=True
    )

    measurement: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
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

    send: Mapped[bool] = mapped_column(
        nullable=False
    )

    invoice_id: Mapped[int | None] = mapped_column(
        ForeignKey("invoices.id", ondelete="SET NULL"),
        nullable=True
    )

    label_type: Mapped[str | None] = mapped_column(
        String(250),
        Enum(LabelChoices),
        server_default=LabelChoices.SUBSCRIPTION.value,
        default=LabelChoices.SUBSCRIPTION.value,
    )

    request_id: Mapped[str | None] = mapped_column(
        String(40),
        nullable=True
    )

    check_url: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    error: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    error_check: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_terminal_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    corrected: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    correct_id: Mapped[int | None] = mapped_column(
        ForeignKey("checks.id", ondelete="SET NULL"),
        nullable=True
    )
