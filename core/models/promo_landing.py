from sqlalchemy.orm import Mapped, mapped_column
from core.models import Base


class Promo_landing(Base):
    promo_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    land_id: Mapped[int | None] = mapped_column(
        nullable=True
    )
