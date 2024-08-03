from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from core.models import Base


class AcquBank(Base):
    code: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    name: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    title: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
