from typing import TYPE_CHECKING

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum

if TYPE_CHECKING:
    from .event import Event
    from .stream import Stream


class MethodChoices(enum.Enum):
    GET = "GET"
    POST = "POST"


class StatusChoices(enum.Enum):
    ACTIVE = "Активный"
    DELETE = "Удаленный"


class Postback(Base):

    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"),
        nullable=True,
    )
    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"),
        nullable=True,
    )
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    method: Mapped[str] = mapped_column(
        String(10),
        Enum(MethodChoices),
        nullable=False,
    )
    event_id: Mapped[list["Event"] | None] = relationship(
        secondary="events_of_the_postback_association",
        back_populates="postbacks_id",
    )

    link: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )
    postdata: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(15),
        Enum(StatusChoices),
        server_default=StatusChoices.ACTIVE.value,
        default=StatusChoices.ACTIVE.value,
        nullable=False,
    )

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
    )

    created_day: Mapped[date] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )

    created_hour: Mapped[str] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )

    change_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=None,
        default=None,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    change_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        server_default=None,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
        nullable=True,
    )

    change_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        server_default=None,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
        nullable=True,
    )
    # Заполняется через Stream
    streams_id: Mapped[list["Stream"] | None] = relationship(
        secondary="streams_of_the_postback_association",
        back_populates="postback_id",
    )
