import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, text, Date, DateTime, ForeignKey, Uuid
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func
import uuid

import enum


class DeviceChoices(enum.Enum):
    MOBILE = "MOBILE"
    DESKTOP = "DESKTOP"


class Host(Base):
    uuid: Mapped[uuid] = mapped_column(Uuid, nullable=False)

    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"), nullable=True
    )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"), nullable=True
    )

    stream_id: Mapped[int | None] = mapped_column(
        ForeignKey("streams.id", ondelete="SET NULL"), nullable=True
    )

    landing_id: Mapped[int | None] = mapped_column(
        ForeignKey("landings.id", ondelete="SET NULL"), nullable=True
    )

    n_partner_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_manager_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_stream_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_landing_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_offer_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    version: Mapped[int | None] = mapped_column(nullable=True)

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

    country_id: Mapped[str | None] = mapped_column(String(500), nullable=True)

    os_id: Mapped[str | None] = mapped_column(String(500), nullable=True)

    device_type: Mapped[str | None] = mapped_column(
        String(50),
        Enum(DeviceChoices),
        server_default=DeviceChoices.DESKTOP.value,
        default=DeviceChoices.DESKTOP.value,
    )

    browser_id: Mapped[str | None] = mapped_column(String(100), nullable=True)

    ref_domain_id: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    referrer_id: Mapped[str | None] = mapped_column(String(2000), nullable=True)

    ipv4: Mapped[str | None] = mapped_column(String(100), nullable=True)

    utm_source: Mapped[str | None] = mapped_column(String(500), nullable=True)

    utm_medium: Mapped[str | None] = mapped_column(String(500), nullable=True)

    utm_campaign: Mapped[str | None] = mapped_column(String(500), nullable=True)

    utm_content: Mapped[str | None] = mapped_column(String(500), nullable=True)

    utm_term: Mapped[str | None] = mapped_column(String(500), nullable=True)

    sub_1: Mapped[str | None] = mapped_column(String(255), nullable=True)

    sub_2: Mapped[str | None] = mapped_column(String(255), nullable=True)

    sub_3: Mapped[str | None] = mapped_column(String(255), nullable=True)

    sub_4: Mapped[str | None] = mapped_column(String(255), nullable=True)

    sub_5: Mapped[str | None] = mapped_column(String(255), nullable=True)

    click_id: Mapped[str | None] = mapped_column(String(500), nullable=True)
