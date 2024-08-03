from typing import TYPE_CHECKING
from typing import List

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Enum, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum

if TYPE_CHECKING:
    from .partner import Partner
    from .offer import Offer


class RoleManagerChoices(enum.Enum):
    OWNER = "OWNER"
    AFFILIATE_MAJOR = "AFFILIATE_MAJOR"
    AFFILIATE_REGULAR = "AFFILIATE_REGULAR"
    OPERATOR = "OPERATOR"
    AUTHOR = "AUTHOR"


class Manager(Base):
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
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")),
    )
    change_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )
    change_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )
    email_verified: Mapped[bool] = mapped_column(
        server_default=text("0"),
        default=False,
    )
    user_is_active: Mapped[bool] = mapped_column(
        server_default="1",
        default=True,
    )
    role: Mapped[str | None] = mapped_column(
        String(100),
        Enum(RoleManagerChoices),
        server_default=RoleManagerChoices.AFFILIATE_REGULAR.value,
        default=RoleManagerChoices.AFFILIATE_REGULAR.value,
    )
    can_edit_offers: Mapped[int] = mapped_column(
        server_default=text("0"),
        nullable=True,
        default=0,
    )
    can_pay: Mapped[int] = mapped_column(
        server_default=text("0"),
        nullable=True,
        default=0,
    )

    partners_id: Mapped[list["Partner"] | None] = relationship(
        back_populates="managers_id",
        secondary="partners_of_the_manager_association",
    )
    # offers: Mapped[list["Offer"] | None] = relationship(
    #     back_populates="manager",
    # )

    def __str__(self):
        if self.email:
            return f"{self.id} {self.email}"
        if self.phone:
            return f"{self.id} {self.phone}"
        return f"{self.id} {self.name}"
