from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from fastapi import Path, Depends, HTTPException, status

from core.models import db_helper
from . import crud


async def payout_req_by_id(
    payout_req_id: Annotated[int, Path(gt=0)],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    payout_req = await crud.get_payoutreq(session=session, payoutreq_id=payout_req_id)
    if not payout_req:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Реквизит с id {payout_req_id} не найден",
        )
    return payout_req
