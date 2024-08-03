from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def kassa_by_id(
    kassa_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    try:
        kassa = await crud.get_kassa(session=session, kassa_id=kassa_id)
    except:
        kassa = None

    if kassa is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"kassa с id {kassa_id} не найден",
        )
    return kassa
