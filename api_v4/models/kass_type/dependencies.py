from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def kass_type_by_id(
    kass_type_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    kass_type = await crud.get_kass_type(session=session, kass_type_id=kass_type_id)
    if not kass_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"kass_type с id {kass_type_id} не найден",
        )
    return kass_type
