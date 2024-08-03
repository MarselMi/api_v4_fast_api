from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def stream_by_id(
    stream_id: Annotated[int, Path(ge=1)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    stream = await crud.get_stream(session=session, stream_id=stream_id)
    if not stream:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"stream с id {stream_id} не найден",
        )
    return stream
