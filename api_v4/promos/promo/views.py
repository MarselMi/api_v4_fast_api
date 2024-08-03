from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.models import db_helper
from . import crud
from schemas import Promo, BasePromo
from dependencies import promo_by_id


router = APIRouter(tags=["Promo"])


@router.get("/", response_model=List[Promo])
async def get_promos(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_promos(session=session)


@router.post("/", response_model=Promo, status_code=status.HTTP_201_CREATED)
async def create_promo(
    promo_in: BasePromo,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_promo(session=session, promo_in=promo_in)


@router.get("/{promo_id}/", response_model=Promo)
async def get_partner(promo: Promo = Depends(promo_by_id)):
    return promo


@router.patch("/{promo_id}/", response_model=Promo)
async def update_partner(
    promo_update: BasePromo,
    promo: Promo = Depends(promo_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_promo(
        session=session,
        promo=promo,
        promo_update=promo_update,
    )
