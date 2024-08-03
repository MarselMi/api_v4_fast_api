from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def prelanding_by_id(
    prelanding_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    prelanding = await crud.get_prelanding(session=session, prelanding_id=prelanding_id)
    if not prelanding:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"prelanding с id {prelanding_id} не найден",
        )
    return prelanding
