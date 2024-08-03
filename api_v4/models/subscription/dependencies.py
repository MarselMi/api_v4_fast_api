from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def subscription_by_id(
    subscription_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    subscription = await crud.get_subscription(
        session=session, subscription_id=subscription_id
    )
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"subscription с id {subscription_id} не найден",
        )
    return subscription
