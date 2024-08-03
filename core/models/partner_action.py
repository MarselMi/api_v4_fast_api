import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, text, Date, DateTime
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func


class PartnerAction(Base):
    act_type: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    manager: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    partner: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
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

    ip: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    action: Mapped[str | None] = mapped_column(
        Text,
        nullable=False
    )
