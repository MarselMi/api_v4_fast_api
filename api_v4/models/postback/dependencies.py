from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def postback_by_id(
    postback_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    postback = await crud.get_postback(session=session, postback_id=postback_id)
    if not postback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"postback с id {postback_id} не найден",
        )
    return postback
