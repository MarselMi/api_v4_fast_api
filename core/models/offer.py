from typing import TYPE_CHECKING
import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum

if TYPE_CHECKING:
    from .partner import Partner
    from .manager import Manager
    from .landing import Landing
    from .prelanding import Prelanding


class StatusChoices(enum.Enum):
    ACTIVE = "Активный"
    DISABLE = "Отключен"
    DELETE = "Удален"


class TypeChoices(enum.Enum):
    PUBLIC = "Публичный"
    PRIVATE = "Приватный"


class CurrencyChoices(enum.Enum):
    RUR = "RUR"
    USD = "USD"
    EUR = "EUR"


class Offer(Base):
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    logo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    geo: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    deduction: Mapped[float] = mapped_column(
        nullable=False,
        default=False,
        server_default="0",
    )
    rebill: Mapped[float] = mapped_column(
        nullable=False,
    )
    trial: Mapped[int] = mapped_column(
        nullable=False,
    )
    payments_periodicity: Mapped[int] = mapped_column(
        nullable=False,
    )
    unexepted_traffic: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    main_domain: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )
    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )
    screenshot: Mapped[str] = mapped_column(
        Text,
        nullable=True,
    )
    status: Mapped[str] = mapped_column(
        String(100),
        Enum(StatusChoices),
        default=StatusChoices.ACTIVE.value,
        server_default=StatusChoices.ACTIVE.value,
    )
    type: Mapped[str] = mapped_column(
        String(100),
        Enum(TypeChoices),
        default=TypeChoices.PUBLIC.value,
        server_default=TypeChoices.PUBLIC.value,
    )
    author_pay: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
    )
    subs_pay: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
    )
    author_percent: Mapped[float] = mapped_column(
        default=0,
        server_default=text("0"),
    )
    first_pay: Mapped[float] = mapped_column(
        default=1,
        server_default=text("1"),
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
        DateTime,
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).now,
    )
    change_date_day: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )
    change_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        server_default=None,
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )
    cash_register_number: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )
    inn: Mapped[str | None] = mapped_column(
        String(12),
        nullable=True,
    )
    rebill_low: Mapped[float | None] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=True,
    )
    rebill_low_period: Mapped[float | None] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=True,
    )
    conf_data: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    user_stats_reports: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
    )
    payment_place: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )
    payment_description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    currency: Mapped[str] = mapped_column(
        String(5),
        Enum(CurrencyChoices),
        default=CurrencyChoices.RUR.value,
        server_default=CurrencyChoices.RUR.value,
    )

    # default_terminal_id: Mapped[int | None] = mapped_column(
    #     ForeignKey("terminals.id", ondelete="SET NULL"),
    #     server_default=None,
    #     default=None,
    #     nullable=True,
    # )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"),
        nullable=True,
    )

    # manager: Mapped["Manager"] = relationship(
    #     back_populates="offers",
    # )

    private_partners: Mapped[list["Partner"] | None] = relationship(
        back_populates="offers_private",
        secondary="partners_of_the_offer_association",
    )

    # landings: Mapped[list["Landing"] | None] = relationship(
    #     back_populates="offer",
    # )

    # prelandings: Mapped[list["Prelanding"] | None] = relationship(
    #     back_populates="offer"
    # )
