import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text, Text, Date, DateTime
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func


class OperatorAction(Base):
    manager_id: Mapped[int | None] = mapped_column(
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

    client_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    phone: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    card: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    action: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
