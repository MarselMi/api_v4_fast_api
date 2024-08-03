from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def error_by_id(
    error_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    error = await crud.get_error(session=session, error_id=error_id)
    if not error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"error с id {error_id} не найден",
        )
    return error
