from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def terminal_by_id(
    terminal_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    terminal = await crud.get_terminal(session=session, terminal_id=terminal_id)
    if not terminal:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"terminal с id {terminal_id} не найден",
        )
    return terminal
