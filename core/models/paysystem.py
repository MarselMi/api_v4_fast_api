from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models import Base


class Paysystem(Base):
    code: Mapped[str] = mapped_column(
        String(250),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
