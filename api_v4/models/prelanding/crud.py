from fastapi import status, HTTPException

from sqlalchemy.orm import selectinload

from core.models import Offer, Partner
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from .schemas import PrelandingCreate, PrelandingUpdate, PrelandingRel
from core.models import Prelanding


async def get_prelandings(
    session: AsyncSession,
) -> List[Prelanding]:
    stmt = (
        select(Prelanding).options(selectinload(Prelanding.private_partners))
        # .options(selectinload(Prelanding.offer))
        .order_by(Prelanding.id)
    )
    result: Result = await session.execute(stmt)
    prelandings = result.scalars().all()
    return list(prelandings)


async def get_prelanding(
    session: AsyncSession,
    prelanding_id: int,
) -> PrelandingRel | None:

    query = (
        select(Prelanding).options(selectinload(Prelanding.private_partners))
        # .options(selectinload(Prelanding.offer))
        .filter(Prelanding.id == prelanding_id)
    )

    result = await session.scalar(query)
    return result


async def create_prelanding(
    session: AsyncSession,
    prelanding_in: PrelandingCreate,
) -> Prelanding:

    offer = await session.get(Offer, prelanding_in.offer_id)
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"offer с id {prelanding_in.offer_id} не найден",
        )

    partners_list = []
    if prelanding_in.private_partners:
        for partner_id in prelanding_in.private_partners:
            stmt = select(Partner).filter(Partner.id == partner_id)
            partner: Partner = await session.scalar(stmt)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
    prelanding_in.private_partners = partners_list

    prelanding = Prelanding(**prelanding_in.model_dump())

    session.add(prelanding)
    await session.commit()
    return prelanding


async def update_prelanding(
    session: AsyncSession,
    prelanding: Prelanding,
    prelanding_update: PrelandingUpdate,
) -> Prelanding:

    if prelanding_update.private_partners:
        partners_list = []
        for partner_id in prelanding_update.private_partners:
            query = select(Partner).where(Partner.id == partner_id)
            partner: Partner = await session.scalar(query)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
        prelanding_update.private_partners = partners_list

    offer = await session.get(Offer, prelanding_update.offer_id)
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"offer с id {prelanding_update.offer_id} не найден",
        )

    # if prelanding_update.offer_id:
    #     query = select(Offer).where(Offer.id == prelanding_update.offer_id)
    #     offer: Offer = await session.scalar(query)
    #     prelanding_update.offer = OfferMin.model_validate(offer, from_attributes=True)

    for key, val in prelanding_update.model_dump(exclude_unset=True).items():
        setattr(prelanding, key, val)

    await session.commit()
    return prelanding
