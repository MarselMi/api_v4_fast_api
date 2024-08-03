from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.models import Base


class AutoUnsub(Base):
    error: Mapped[str] = mapped_column(
        String(300),
        nullable=False
    )

    ps: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )
