from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from core.models import Base

if TYPE_CHECKING:
    from .kassa import Kassa


class Organisation(Base):
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    inn: Mapped[str] = mapped_column(String(20), nullable=False)

    # kassa: Mapped["Kassa"] = relationship(back_populates="organisation")
