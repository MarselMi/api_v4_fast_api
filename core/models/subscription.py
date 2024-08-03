import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum


class StatusChoices(enum.Enum):
    AWAIT = "AWAIT"
    BAD = "BAD"
    ACTIVE = "ACTIVE"
    CANCELLED = "CANCELLED"


class TypeChoices(enum.Enum):
    standart = "standart"
    height = "height"
    lower = "lower"


class UnsubChoices(enum.Enum):
    client = "client"
    operator = "operator"
    manager = "manager"
    auto = "auto"


class Subscription(Base):
    client_id: Mapped[int | None] = mapped_column(
        ForeignKey("clients.id", ondelete="SET NULL"), nullable=True
    )

    type: Mapped[str | None] = mapped_column(
        String(100),
        Enum(TypeChoices),
        server_default=TypeChoices.standart.value,
        default=TypeChoices.standart.value,
    )

    now_type: Mapped[int] = mapped_column(
        default=1, server_default=text("1"), nullable=False
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

    create_date_hour: Mapped[int | None] = mapped_column(
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
        nullable=True,
    )

    unsub_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        # server_default=func.now(),
        default=None,
        nullable=True,
    )

    unsub_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    unsub_date_hour: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )

    is_unsub: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    tarif_name: Mapped[str] = mapped_column(String(250), nullable=False)

    two_tarif_name: Mapped[str | None] = mapped_column(String(250), nullable=True)

    tarif_sum: Mapped[float] = mapped_column(nullable=False)

    two_tarif_sum: Mapped[float | None] = mapped_column(nullable=True)

    status: Mapped[str | None] = mapped_column(
        String(20),
        Enum(StatusChoices),
        server_default=StatusChoices.ACTIVE.value,
        default=StatusChoices.ACTIVE.value,
    )

    start_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        # server_default=func.now(),
        default=None,
        nullable=True,
    )

    start_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    start_date_hour: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )

    is_start: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    try_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        # server_default=func.now(),
        default=None,
        nullable=True,
    )

    try_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    try_date_hour: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )

    two_try_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        # server_default=func.now(),
        default=None,
        nullable=True,
    )

    two_try_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    two_try_date_hour: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )

    pay_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        # server_default=func.now(),
        default=None,
        nullable=True,
    )

    pay_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    pay_date_hour: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )

    two_pay_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        # server_default=func.now(),
        default=None,
        nullable=True,
    )

    two_pay_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    two_pay_date_hour: Mapped[int | None] = mapped_column(
        default=None,
        nullable=True,
    )

    try_count: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    two_try_count: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    count_fail: Mapped[int | None] = mapped_column(nullable=True)

    period: Mapped[int] = mapped_column(nullable=False)

    two_period: Mapped[int | None] = mapped_column(nullable=True)

    freeday: Mapped[int | None] = mapped_column(nullable=True)

    two_freeday: Mapped[int | None] = mapped_column(nullable=True)

    transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("incomingtransactions.id", ondelete="SET NULL"), nullable=True
    )

    card_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    token: Mapped[str | None] = mapped_column(String(255), nullable=True)
    count_good: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    time_good: Mapped[float] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_client_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_host_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_partner_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_stream_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_offer_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_landing_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_manager_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_terminal_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    profit: Mapped[float] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    type_unsub: Mapped[str | None] = mapped_column(
        String(100),
        Enum(UnsubChoices),
        server_default=UnsubChoices.client.value,
        default=UnsubChoices.client.value,
    )

    type_unsub_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    type_unsub_val: Mapped[int | None] = mapped_column(nullable=True)

    terminal_id: Mapped[int | None] = mapped_column(
        ForeignKey("terminals.id", ondelete="SET NULL"), nullable=True
    )

    added_rebill_period: Mapped[int | None] = mapped_column(nullable=True)

    error: Mapped[int | None] = mapped_column(
        ForeignKey("transactionerrors.id", ondelete="SET NULL"), nullable=True
    )

    try_interval_days: Mapped[int] = mapped_column(
        default=4, server_default=text("4"), nullable=False
    )

    try_interval_days_def: Mapped[int] = mapped_column(
        default=4, server_default=text("4"), nullable=False
    )

    is_tariff_updated: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )
