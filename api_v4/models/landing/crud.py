from fastapi import HTTPException, status
from sqlalchemy.orm import selectinload

from core.models import Offer, Partner
from core.models import Landing
from core.models import LandingElement

from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from .schemas import LandingCreate, LandingUpdate


async def get_landings(
    session: AsyncSession,
) -> List[Landing]:
    query = (
        select(Landing).options(selectinload(Landing.private_partners))
        # .options(selectinload(Landing.offer))
        # .options(selectinload(Landing.land_elements))
        .order_by(Landing.id)
    )
    result: Result = await session.execute(query)
    landings = result.scalars().all()
    return list(landings)


async def get_landing(
    session: AsyncSession,
    landing_id: int,
) -> Landing | None:

    query = (
        select(Landing).options(selectinload(Landing.private_partners))
        # .options(selectinload(Landing.offer))
        # .options(selectinload(Landing.landing_elements))
        .filter(Landing.id == landing_id)
    )
    result = await session.scalar(query)
    if result is not None:
        land_elements = await session.get(LandingElement, result.landing_elements)
        if land_elements:
            result.elements = land_elements.elements
    return result


async def create_landing(
    session: AsyncSession,
    landing_in: LandingCreate,
) -> Landing:

    offer = await session.get(Offer, landing_in.offer_id)
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"offer с id {landing_in.offer_id} не найден",
        )

    if landing_in.landing_elements:
        element = await session.get(LandingElement, landing_in.landing_elements)
        if element is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"landing_elements с id {landing_in.landing_elements} не найден",
            )

    partners_list = []
    if landing_in.private_partners:
        for partner_id in landing_in.private_partners:
            query = select(Partner).filter(Partner.id == partner_id)
            partner: Partner = await session.scalar(query)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
    landing_in.private_partners = partners_list

    landing = Landing(**landing_in.model_dump())

    session.add(landing)
    await session.commit()
    return landing


async def update_landing(
    session: AsyncSession,
    landing: Landing,
    landing_update: LandingUpdate,
) -> Landing:

    if landing_update.private_partners:
        partners_list = []
        for partner_id in landing_update.private_partners:
            query = select(Partner).where(Partner.id == partner_id)
            partner: Partner = await session.scalar(query)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
        landing_update.private_partners = partners_list

    if landing_update.landing_elements:
        element = await session.get(LandingElement, landing_update.landing_elements)
        if element is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"landing_elements с id {landing_update.landing_elements} не найден",
            )

    offer = await session.get(Offer, landing_update.offer_id)
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"offer с id {landing_update.offer_id} не найден",
        )
    # if landing_update.offer_id:
    #     query = select(Offer).where(Offer.id == landing_update.offer_id)
    #     offer: Offer = await session.scalar(query)
    #     landing_update.offer = OfferMin.model_validate(offer, from_attributes=True)

    for key, val in landing_update.model_dump(exclude_unset=True).items():
        setattr(landing, key, val)

    await session.commit()
    return landing
