import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Text, text, Date, DateTime, ForeignKey, Uuid
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func
import uuid

import enum


class StatusChoices(enum.Enum):
    ACTIVE = "Активный"
    BLOCK = "Заблокирован"
    DELETE = "Удален"


class Client(Base):
    uuid: Mapped[uuid] = mapped_column(Uuid, nullable=False)

    email: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
        # unique=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    password: Mapped[str] = mapped_column(
        String(200),
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

    change_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        default=None,
        nullable=True,
    )

    change_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    change_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
    )

    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"), nullable=True
    )

    host_id: Mapped[int | None] = mapped_column(
        ForeignKey("hosts.id", ondelete="SET NULL"), nullable=True
    )

    status: Mapped[str | None] = mapped_column(
        String(50),
        Enum(StatusChoices),
        server_default=StatusChoices.ACTIVE.value,
        default=StatusChoices.ACTIVE.value,
    )

    last_auth_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    last_auth_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    last_auth_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
    )

    first_subscribe_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    first_subscribe_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    first_subscribe_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
    )

    is_subscribed: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    data: Mapped[str | None] = mapped_column(Text, nullable=True)

    n_partner_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_host_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_stream_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_landing_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_manager_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    n_offer_id: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    active: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    card_first_six: Mapped[str | None] = mapped_column(String(10), nullable=True)

    card_last_four: Mapped[str | None] = mapped_column(String(10), nullable=True)

    technical: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    tech_show: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    note: Mapped[str | None] = mapped_column(Text, nullable=True)

    last_call: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    charge_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )

    tech_reb_count: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    contacts: Mapped[str | None] = mapped_column(Text, nullable=True)

    pre_payment_request: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        default=None,
        nullable=True,
    )
