from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, text, ForeignKey, Uuid
from core.models import Base
from uuid import uuid4

import enum

if TYPE_CHECKING:
    from .stream import Stream
    from .partner import Partner
    from .offer import Offer
    from .landing import Landing


class StatusChoices(enum.Enum):
    NO_PROCESS = "NO_PROCESS"
    PROCESSED = "PROCESSED"
    NO_POSTBACK = "NO_POSTBACK"
    NO_POSTBACK_EVENT = "NO_POSTBACK_EVENT"
    SENT = "SENT"


class PostbackEvent(Base):
    stream_id: Mapped[int | None] = mapped_column(
        ForeignKey("streams.id", ondelete="SET NULL"), nullable=True
    )

    # streams: Mapped["Stream"] = relationship(
    #     back_populates="streams"
    # )

    payout: Mapped[float] = mapped_column(nullable=True)

    transaction_id: Mapped[uuid4] = mapped_column(Uuid(), nullable=False)

    type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"), nullable=True
    )

    # partners: Mapped["Partner"] = relationship(
    #     back_populates="partners"
    # )

    offer_id: Mapped[int | None] = mapped_column(
        ForeignKey("offers.id", ondelete="SET NULL"), nullable=True
    )

    # offers: Mapped["Offer"] = relationship(
    #     back_populates="offers"
    # )

    landing_id: Mapped[int | None] = mapped_column(
        ForeignKey("landings.id", ondelete="SET NULL"), nullable=True
    )

    # landings: Mapped["Landing"] = relationship(
    #     back_populates="landings"
    # )

    status: Mapped[str | None] = mapped_column(
        String(50),
        Enum(StatusChoices),
        server_default=StatusChoices.NO_PROCESS.value,
        default=StatusChoices.NO_PROCESS.value,
    )

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

    n_subscription_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_client_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_host_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_partner_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_stream_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_offer_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )

    n_landing_id: Mapped[int] = mapped_column(
        nullable=False, default=0, server_default=text("0")
    )
