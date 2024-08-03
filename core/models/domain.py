import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, Text, Date, DateTime
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func


class Domain(Base):
    domain: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
    )

    create_date_day: Mapped[date] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )

    create_date_hour: Mapped[str] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )

    select_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=None,
        nullable=True,
    )

    select_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    select_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
    )

    turn_off_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=None,
        nullable=True,
    )

    turn_off_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
    )

    turn_off_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
    )

    is_select: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    is_delete: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

