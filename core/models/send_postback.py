from typing import TYPE_CHECKING

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, text, Date, Text, ForeignKey
from core.models import Base
from datetime import datetime, date

import enum

if TYPE_CHECKING:
    from .postback_event import PostbackEvent
    from .postback import Postback


class StatusChoices(enum.Enum):
    await_ = "await"
    sent = "sent"


class TypeChoices(enum.Enum):
    GET = "GET"
    POST = "POST"


class SendPostback(Base):
    status: Mapped[str | None] = mapped_column(
        String(50),
        Enum(StatusChoices),
        server_default=StatusChoices.await_.value,
        default=StatusChoices.await_.value,
    )

    create_date: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
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

    send_date: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )

    send_date_day: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )

    send_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        server_default=None,
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )

    type: Mapped[str | None] = mapped_column(
        String(10),
        Enum(TypeChoices),
        server_default=TypeChoices.GET.value,
        default=TypeChoices.GET.value,
    )

    url: Mapped[str | None] = mapped_column(Text, nullable=True)

    send_data: Mapped[str | None] = mapped_column(Text, nullable=True)

    response: Mapped[str | None] = mapped_column(Text, nullable=True)

    send_event_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    postback_event_id: Mapped[int | None] = mapped_column(
        ForeignKey("postbackevents.id", ondelete="SET NULL"), nullable=True
    )

    # postbackevents: Mapped["PostbackEvent"] = relationship(
    #     back_populates="postbackevents"
    # )

    postback_id: Mapped[int | None] = mapped_column(
        ForeignKey("postbacks.id", ondelete="SET NULL"), nullable=True
    )

    # postbacks: Mapped["Postback"] = relationship(
    #     back_populates="postbacks"
    # )

    data: Mapped[str | None] = mapped_column(Text, nullable=True)

    bad_url: Mapped[int] = mapped_column(
        default=0, server_default=text("0"), nullable=False
    )
