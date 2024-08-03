from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def invoice_by_id(
        invoice_id: Annotated[int, Path(ge=1)],
        session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    invoice = await crud.get_invoice(session=session, invoice_id=invoice_id)
    if not invoice:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Инвойс с id {invoice_id} не найден",
        )
    return invoice
