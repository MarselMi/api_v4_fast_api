from typing import TYPE_CHECKING

from core.models import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from .postback import Postback


class Event(Base):
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    postbacks_id: Mapped[list["Postback"]] = relationship(
        secondary="events_of_the_postback_association",
        back_populates="event_id",
    )
