from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey
from core.models import Base


class IncomingTransactionID(Base):
    incoming_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    incoming_id_text: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    incoming_transaction_id: Mapped[int | None] = mapped_column(
        ForeignKey("incomingtransactions.id", ondelete="SET NULL"),
        nullable=True
    )
