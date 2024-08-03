from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models import Base


class OS(Base):
    name: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )
