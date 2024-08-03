from core.models import KassType
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import KassTypeCreate


async def get_kass_types(session: AsyncSession) -> List[KassType]:
    query = select(KassType).order_by(KassType.id)
    result: Result = await session.execute(query)
    kass_type = result.scalars().all()
    return list(kass_type)


async def get_kass_type(session: AsyncSession, kass_type_id: int) -> KassType | None:
    return await session.get(KassType, kass_type_id)


async def create_kass_type(
    session: AsyncSession, kass_type_in: KassTypeCreate
) -> KassType:
    kass_type_in = kass_type_in.model_dump()
    kass_type = KassType(**kass_type_in)
    session.add(kass_type)
    await session.commit()
    return kass_type
