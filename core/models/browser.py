from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models import Base


class Browser(Base):
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
