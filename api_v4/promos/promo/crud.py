from core.models import Promo
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import BasePromo


async def get_promos(
    session: AsyncSession,
) -> List[Promo]:
    query = select(Promo).order_by(Promo.id)
    result: Result = await session.execute(query)
    promos = result.scalars().all()
    return list(promos)


async def get_promo(
    session: AsyncSession,
    promo_id: int,
) -> Promo | None:
    return await session.get(Promo, promo_id)


async def create_promo(
    session: AsyncSession,
    promo_in: BasePromo,
) -> Promo:
    promo_in = promo_in.model_dump()
    promo = Promo(**promo_in)
    session.add(promo)
    await session.commit()
    return promo


async def update_promo(
    session: AsyncSession,
    promo_update: BasePromo,
    promo: Promo,
):
    for name, value in promo_update.model_dump(exclude_unset=True).items():
        setattr(promo, name, value)
    await session.commit()

    return promo
