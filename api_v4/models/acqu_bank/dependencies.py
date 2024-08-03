from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def acqu_bank_by_id(
    acqu_bank_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    acqu_bank = await crud.get_acqu_bank(session=session, acqu_bank_id=acqu_bank_id)
    if not acqu_bank:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"acqu_bank с id {acqu_bank_id} не найден",
        )
    return acqu_bank
