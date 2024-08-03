from core.models import Paysystem
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import PaySystemCreate


async def get_paysystems(
    session: AsyncSession,
) -> List[Paysystem]:
    query = select(Paysystem).order_by(Paysystem.id)
    result: Result = await session.execute(query)
    event = result.scalars().all()
    return list(event)


async def get_paysystem(
    session: AsyncSession,
    paysystem_id: int,
) -> Paysystem | None:
    return await session.get(Paysystem, paysystem_id)


async def create_paysystem(
    session: AsyncSession,
    paysystem_in: PaySystemCreate,
) -> Paysystem:

    paysystem = Paysystem(**paysystem_in.model_dump())
    session.add(paysystem)
    await session.commit()
    return paysystem
