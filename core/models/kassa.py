from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, text, ForeignKey
from core.models import Base

if TYPE_CHECKING:
    from .organisation import Organisation


class Kassa(Base):
    number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )
    status: Mapped[int | None] = mapped_column(
        default=2,
        server_default=text("2"),
        nullable=True,
    )
    used_in_pay: Mapped[int | None] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=True,
    )
    login: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )
    password: Mapped[str | None] = mapped_column(
        String(250),
        nullable=True,
    )
    kass_type: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    organisation_id: Mapped[int | None] = mapped_column(
        ForeignKey("organisations.id", ondelete="SET NULL"),
        nullable=True,
    )
    # organisation: Mapped["Organisation"] = relationship(back_populates="kassa")
