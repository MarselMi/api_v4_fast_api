import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, Text, DateTime, Enum
from core.models import Base
from datetime import datetime
from sqlalchemy.sql import func

import enum


class StatusActions(enum.Enum):
    active = "active"
    await_ = "await"
    block = "block"
    del_ = "del"


class ModerationActions(enum.Enum):
    await_ = "await"
    active = "active"
    cancelled = "cancelled"


class Promo_data(Base):
    promo_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    partner_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    name: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    created_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    status: Mapped[str | None] = mapped_column(
        String(100),
        Enum(StatusActions),
        server_default=StatusActions.active.value,
        default=StatusActions.active.value,
    )

    moderation: Mapped[str | None] = mapped_column(
        String(100),
        Enum(ModerationActions),
        server_default=ModerationActions.await_.value,
        default=ModerationActions.await_.value,
    )

    is_worked: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    create_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    new_value: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
