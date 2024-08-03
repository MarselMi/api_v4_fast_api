import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, text, Date, DateTime, Text
from core.models import Base
from datetime import datetime
from sqlalchemy.sql import func

import enum


class StatusChoices(enum.Enum):
    ROUGH_COPY = "ROUGH_COPY"
    PUBLISH = "PUBLISH"
    DELETE = "DELETE"


class News(Base):
    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    date_day: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
        nullable=True,
    )

    date_hour: Mapped[str | None] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
        nullable=True,
    )

    status: Mapped[str | None] = mapped_column(
        String(60),
        Enum(StatusChoices),
        server_default=StatusChoices.ROUGH_COPY.value,
        default=StatusChoices.ROUGH_COPY.value,
    )

    icon: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
