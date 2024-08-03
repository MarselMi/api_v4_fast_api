from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper

from .schemas import PayoutRequisite, PaySystemUpdate
from .dependencies import payout_req_by_id
from . import crud


router = APIRouter(tags=["PayOutRequisites"])


@router.get("/", response_model=List[PayoutRequisite])
async def get_payout_req(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_payoutreqs(session=session)


@router.get("/{payout_req_id}/", response_model=PayoutRequisite)
async def get_pay_req(payout_req: PayoutRequisite = Depends(payout_req_by_id)):
    return payout_req


@router.patch("/{payout_req_id}/", response_model=PayoutRequisite)
async def update_pay_req(
    pay_req_in: PaySystemUpdate,
    pay_req: PayoutRequisite = Depends(payout_req_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_payoutreq(
        pay_req_in=pay_req_in,
        pay_req=pay_req,
        session=session,
    )
