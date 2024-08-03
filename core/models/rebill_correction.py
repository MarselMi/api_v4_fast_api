from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import text, DateTime, ForeignKey
from core.models import Base
from datetime import datetime
from sqlalchemy.sql import func


class RebillCorrection(Base):
    terminal_id: Mapped[int | None] = mapped_column(
        ForeignKey("terminals.id", ondelete="SET NULL"),
        nullable=True
    )

    sum: Mapped[float] = mapped_column(
        nullable=False
    )

    quantity: Mapped[float] = mapped_column(
        nullable=False
    )

    pay_per_month: Mapped[float] = mapped_column(
        nullable=False
    )

    can_work: Mapped[int] = mapped_column(
        default=1,
        server_default=text("1"),
        nullable=False
    )

    current_quantity: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    current_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=None,
        nullable=True,
    )

    whole_offer: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    target_terminal: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )
