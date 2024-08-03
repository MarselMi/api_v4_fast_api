from sqlalchemy.orm import selectinload

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError

from sqlalchemy.orm.exc import FlushError

from core.models import Offer, Partner, Manager
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from api_v4.models.partner.schemas import PartnerMin
from .schemas import OfferCreate, OfferUpdate, OfferRel


async def get_offers(session: AsyncSession) -> List[OfferRel]:
    stmt = (
        select(Offer).options(selectinload(Offer.private_partners))
        # .options(selectinload(Offer.manager))
        .order_by(Offer.id)
    )
    result: Result = await session.execute(stmt)
    offer = result.scalars().all()
    return list(offer)


async def get_offer(session: AsyncSession, offer_id: int) -> OfferRel | None:

    query = (
        select(Offer).options(selectinload(Offer.private_partners))
        # .options(selectinload(Offer.manager))
        .filter(Offer.id == offer_id)
    )
    result_query = await session.scalar(query)
    result: OfferRel = OfferRel.model_validate(result_query, from_attributes=True)

    return result


async def create_offer(session: AsyncSession, offer_in: OfferCreate) -> Offer | None:

    partners_list = []
    if offer_in.private_partners:
        for partner_id in offer_in.private_partners:
            stmt = select(Partner).filter(Partner.id == partner_id)
            partner: Partner = await session.scalar(stmt)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
    offer_in.private_partners = partners_list

    if offer_in.manager_id:
        manager = await session.get(Manager, offer_in.manager_id)

        if manager is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"manager с id {offer_in.manager_id} не найден",
            )
    # off_manager = offer_in.manager_id
    # if off_manager:
    #     stmt = select(Manager).filter(Manager.id == offer_in.manager_id)
    #     manager_object: "Manager" = await session.scalar(stmt)

    offer_in = offer_in.model_dump()

    offer = Offer(**offer_in)

    # print(offer)
    # if off_manager:
    #     offer.manager: Manager = manager_object
    session.add(offer)
    await session.commit()
    return offer


async def update_offer(
    session: AsyncSession, offer: Offer, offer_update: OfferUpdate
) -> Offer:

    if offer_update.private_partners:
        partners_list = []
        for partner_id in offer_update.private_partners:
            query = select(Partner).where(Partner.id == partner_id)
            partner: Partner = await session.scalar(query)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partner_validate: PartnerMin = PartnerMin.model_validate(
                    partner, from_attributes=True
                )
                partners_list.append(partner_validate)
        offer_update.private_partners = partners_list

    # if offer_update.manager_id:
    #     query = select(Manager).where(Manager.id == offer_update.manager_id)
    #     manager: Manager = await session.scalar(query)
    #     offer_update.manager = ManagerMin.model_validate(manager, from_attributes=True)

    for key, val in offer_update.model_dump(exclude_unset=True).items():
        setattr(offer, key, val)

    await session.commit()
    return offer
