from typing import TYPE_CHECKING

import pytz
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, text, Text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

if TYPE_CHECKING:
    from .partner import Partner
    from .manager import Manager
    from .landing import Landing
    from .prelanding import Prelanding
    from .postback import Postback
    from .offer import Offer


class Stream(Base):
    name: Mapped[str] = mapped_column(String(250), nullable=False)

    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"), nullable=True
    )

    # partners: Mapped["Partner"] = relationship(
    #     back_populates="partners"
    # )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"), nullable=True
    )

    # managers: Mapped["Manager"] = relationship(
    #     back_populates="managers"
    # )

    landing_id: Mapped[int | None] = mapped_column(
        ForeignKey("landings.id", ondelete="SET NULL"), nullable=True
    )

    # landings: Mapped["Landing"] = relationship(
    #     back_populates="landings"
    # )

    prelanding_id: Mapped[int | None] = mapped_column(
        ForeignKey("prelandings.id", ondelete="SET NULL"), nullable=True
    )

    # prelandings: Mapped["Prelanding"] = relationship(
    #     back_populates="prelandings"
    # )

    uid: Mapped[int] = mapped_column(nullable=False, unique=True)

    postback_id: Mapped[list["Postback"] | None] = relationship(
        back_populates="streams_id",
        secondary="streams_of_the_postback_association",
    )

    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"), nullable=True
    )

    # offers: Mapped["Offer"] = relationship(
    #     back_populates="offers"
    # )

    link: Mapped[str | None] = mapped_column(Text, nullable=True)

    yandex_id: Mapped[str | None] = mapped_column(String(500), nullable=True)

    created_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )
    created_day: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
        nullable=True,
    )
    created_hour: Mapped[str | None] = mapped_column(
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

    yandex_metric: Mapped[str | None] = mapped_column(String(255), nullable=True)

    google_analytics: Mapped[str | None] = mapped_column(String(255), nullable=True)

    top_mail_ru: Mapped[str | None] = mapped_column(String(255), nullable=True)

    facebook_pixel: Mapped[str | None] = mapped_column(String(255), nullable=True)

    vk_counter: Mapped[str | None] = mapped_column(String(255), nullable=True)

    tiktok_pixel: Mapped[str | None] = mapped_column(String(255), nullable=True)

    landingelement_data: Mapped[str | None] = mapped_column(Text, nullable=True)
