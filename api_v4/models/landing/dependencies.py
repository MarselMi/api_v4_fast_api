from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def landing_by_id(
    landing_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    landing = await crud.get_landing(session=session, landing_id=landing_id)
    if not landing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"landing с id {landing_id} не найден",
        )
    return landing
