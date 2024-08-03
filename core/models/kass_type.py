from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Enum
from core.models import Base


import enum


class MethodChoices(enum.Enum):
    API = "API"
    WIDGET = "WIDGET"


class KassType(Base):
    title: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )
    method: Mapped[str | None] = mapped_column(
        String(10),
        Enum(MethodChoices),
        default=MethodChoices.API.value,
        server_default=MethodChoices.API.value,
    )
    link: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
