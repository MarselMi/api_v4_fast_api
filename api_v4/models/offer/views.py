from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import OfferCreate, Offer, OfferUpdate
from .dependencies import offer_by_id
from . import crud

router = APIRouter(tags=["Offers"])


@router.get("/", response_model=List[Offer])
async def get_offers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_offers(session=session)


@router.post("/", response_model=Offer, status_code=status.HTTP_201_CREATED)
async def create_offer(
    offer_in: OfferCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    offer = await crud.create_offer(session=session, offer_in=offer_in)
    return offer


@router.get("/{offer_id}/", response_model=Offer)
async def get_offer(offer: Offer = Depends(offer_by_id)):
    return offer


@router.patch("/{offer_id}/", response_model=Offer)
async def update_offer(
    offer_update: OfferUpdate,
    offer: Offer = Depends(offer_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_offer(
        session=session,
        offer=offer,
        offer_update=offer_update,
    )
