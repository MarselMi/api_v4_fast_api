from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def paysystem_by_id(
    paysystem_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    paysystem = await crud.get_paysystem(session=session, paysystem_id=paysystem_id)
    if not paysystem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"paysystem с id {paysystem_id} не найден",
        )
    return paysystem
