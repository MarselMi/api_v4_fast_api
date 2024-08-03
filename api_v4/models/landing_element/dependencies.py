from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def land_element_by_id(
    land_element_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    land_element = await crud.get_land_element(
        session=session, land_element_id=land_element_id
    )
    if not land_element:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"land_element с id {land_element_id} не найден",
        )
    return land_element
