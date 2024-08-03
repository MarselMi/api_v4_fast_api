from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models import Base


class Referrer(Base):
    name: Mapped[str] = mapped_column(
        String(5000),
        nullable=False
    )
