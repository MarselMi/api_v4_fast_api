from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from core.models import Base


class Bank(Base):
    banks: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
