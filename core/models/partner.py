from typing import TYPE_CHECKING

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum

if TYPE_CHECKING:
    from .manager import Manager
    from .landing import Landing
    from .offer import Offer
    from .prelanding import Prelanding


class ThemeChoices(enum.Enum):
    LIGHT = "Светлая"
    DARK = "Темная"


class RoleChoices(enum.Enum):
    OWNER = "OWNER"
    AFFILIATE_MAJOR = "AFFILIATE_MAJOR"
    AFFILIATE_REGULAR = "AFFILIATE_REGULAR"
    OPERATOR = "OPERATOR"


class Partner(Base):
    uid: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    email: Mapped[str] = mapped_column(
        String(250),
        unique=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    password: Mapped[str] = mapped_column(
        String(200),
    )

    name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    avatar: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    telegram: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )

    telegram_id: Mapped[int | None] = mapped_column(
        nullable=True,
    )

    percent: Mapped[float | None] = mapped_column(
        server_default=text("50.0"),
        default=50.0,
    )

    referal_fees: Mapped[float | None] = mapped_column(
        nullable=True,
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

    last_activity: Mapped[datetime | None] = mapped_column(
        DateTime,
        default=None,
        nullable=True,
    )

    ip_reg: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    ip_auth: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    referal: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"),
        nullable=True,
    )

    email_verified: Mapped[bool] = mapped_column(
        server_default=text("0"),
        default=False,
    )

    user_is_active: Mapped[bool] = mapped_column(
        server_default="1",
        default=True,
    )

    theme: Mapped[str | None] = mapped_column(
        String(20),
        Enum(ThemeChoices),
        server_default=ThemeChoices.LIGHT.value,
        default=ThemeChoices.LIGHT.value,
    )

    role: Mapped[str | None] = mapped_column(
        String(100),
        Enum(RoleChoices),
        server_default=RoleChoices.AFFILIATE_REGULAR.value,
        default=RoleChoices.AFFILIATE_REGULAR.value,
    )

    is_staff: Mapped[bool] = mapped_column(
        server_default=text("0"),
        default=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        server_default=text("0"),
        default=False,
    )

    want_to_get_notifications: Mapped[bool] = mapped_column(
        server_default=text("1"),
        default=True,
    )

    contest_nick: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    contest_check: Mapped[bool] = mapped_column(
        server_default=text("0"),
        default=False,
    )

    two_factor_auth: Mapped[bool] = mapped_column(
        server_default=text("0"),
        default=False,
    )

    traffic_is_stopped: Mapped[int] = mapped_column(
        server_default=text("0"),
        default=0,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    permanent: Mapped[int] = mapped_column(
        server_default=text("1"),
        default=1,
    )

    temporary_percent: Mapped[float] = mapped_column(
        server_default=text("50.0"),
        default=50.0,
    )

    temporary_start: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
    )

    temporary_end: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
    )

    old_percent: Mapped[float] = mapped_column(
        server_default=text("50.0"),
        default=50.0,
    )

    auto_pay: Mapped[int | None] = mapped_column(
        server_default=text("0"),
        default=0,
        nullable=True,
    )

    auto_pay_limit: Mapped[float | None] = mapped_column(
        server_default=text("0"),
        default=0,
        nullable=True,
    )

    past_auto_pay_limit: Mapped[float | None] = mapped_column(
        server_default=text("0"),
        default=0,
        nullable=True,
    )

    last_auto_pay: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
    )

    offers_private: Mapped[list["Offer"] | None] = relationship(
        back_populates="private_partners",
        secondary="partners_of_the_offer_association",
    )
    landings_private: Mapped[list["Landing"] | None] = relationship(
        back_populates="private_partners",
        secondary="partners_of_the_landings_association",
    )
    prelandings_private: Mapped[list["Prelanding"] | None] = relationship(
        back_populates="private_partners",
        secondary="partners_of_the_prelandings_association",
    )

    managers_id: Mapped[list["Manager"] | None] = relationship(
        back_populates="partners_id",
        secondary="partners_of_the_manager_association",
    )

    def __str__(self):
        if self.email:
            return f"{self.id} {self.email}"
        if self.phone:
            return f"{self.id} {self.phone}"
        return f"{self.id} {self.name}"
