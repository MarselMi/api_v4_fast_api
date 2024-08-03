from core.models import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, DateTime, text
from sqlalchemy.sql import func
from datetime import datetime

import pytz

import enum


class TypeChoices(enum.Enum):
    SUBSCRIPTION = "SUBSCRIPTION"
    REBILL = "REBILL"


class Invoice(Base):
    operation_type: Mapped[int] = mapped_column(
        String(20), Enum(TypeChoices), nullable=False
    )
    operation_id: Mapped[int] = mapped_column(nullable=False)
    create_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=False,
    )
    n_subscription_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
    n_client_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
    n_host_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
    n_partner_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
    n_stream_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
    n_offer_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
    n_landing_id: Mapped[int] = mapped_column(
        server_default=text("0"), default=0, nullable=False
    )
