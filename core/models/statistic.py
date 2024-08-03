from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text
from core.models import Base


class Statistic(Base):
    total_balance: Mapped[float] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    total_balance_usd: Mapped[float] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    total_balance_eur: Mapped[float] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    subscriptions_paid: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    subscriptions_unpaid: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    subscriptions_unsub: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    subscriptions_no_rebill: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )
