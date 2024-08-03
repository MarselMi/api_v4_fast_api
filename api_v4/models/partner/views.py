from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from . import crud
from .schemas import Partner, PartnerCreate, PartnerUpdate
from .dependencies import partner_by_id

router = APIRouter(tags=["Partners"])


@router.get("/", response_model=List[Partner])
async def get_partner(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_partners(session=session)


@router.post("/", response_model=Partner, status_code=status.HTTP_201_CREATED)
async def create_partner(
    partner_in: PartnerCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    partner = await crud.create_partner(session=session, partner_in=partner_in)
    return partner


@router.get("/{partner_id}/", response_model=Partner)
async def get_partner(partner: Partner = Depends(partner_by_id)):
    return partner


@router.patch("/{partner_id}/", response_model=Partner)
async def update_partner(
    partner_update: PartnerUpdate,
    partner: Partner = Depends(partner_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_partner(
        session=session,
        partner=partner,
        partner_update=partner_update,
    )
