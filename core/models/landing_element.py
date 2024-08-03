from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text
from core.models import Base

if TYPE_CHECKING:
    from .landing import Landing


class LandingElement(Base):
    elements: Mapped[str] = mapped_column(Text, nullable=True)

    # landing: Mapped["Landing"] = relationship(back_populates="land_elements")
