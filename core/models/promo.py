from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Text
from core.models import Base

import enum


class TypeChoices(enum.Enum):
    construktor_js = "construktor_js"
    html = "html"


class StatusChoices(enum.Enum):
    show = "show"
    hide = "hide"
    del_ = "del"


class ViewChoices(enum.Enum):
    public = "public"
    private = "private"


class Promo(Base):
    name: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    type: Mapped[str | None] = mapped_column(
        String(100),
        Enum(TypeChoices),
        nullable=True,
    )

    status: Mapped[str | None] = mapped_column(
        String(100),
        Enum(StatusChoices),
        nullable=True,
    )

    view: Mapped[str | None] = mapped_column(
        String(100),
        Enum(ViewChoices),
        nullable=True,
    )

    js_src: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    js: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
