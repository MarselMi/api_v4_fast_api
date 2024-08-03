from sqlalchemy.orm import selectinload

from core.models import Kassa, Organisation
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from fastapi import status, HTTPException

from .schemas import KassaCreate, KassaUpdate


async def get_kasses(
    session: AsyncSession,
) -> List[Kassa]:
    query = select(Kassa).order_by(Kassa.id)

    result: Result = await session.execute(query)
    kassa = result.scalars().all()

    return list(kassa)


async def get_kassa(
    session: AsyncSession,
    kassa_id: int,
) -> Kassa | None:
    query = select(Kassa).filter(Kassa.id == kassa_id)

    result = await session.scalar(query)

    return result


async def create_kassa(
    session: AsyncSession,
    kassa_in: KassaCreate,
) -> Kassa:

    if kassa_in.organisation_id:
        postback = await session.get(Organisation, kassa_in.organisation_id)
        if postback is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"organisation с id {kassa_in.organisation_id} не найден",
            )

    kassa = Kassa(**kassa_in.model_dump())

    session.add(kassa)
    await session.commit()

    return kassa


async def update_kassa(
    session: AsyncSession,
    kassa: Kassa,
    kassa_update: KassaUpdate,
) -> Kassa:

    if kassa_update.organisation_id:

        organisation = await session.get(Organisation, kassa_update.organisation_id)

        if organisation is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"organisation с id {kassa_update.organisation_id} не найден",
            )

    for name, value in kassa_update.model_dump(exclude_unset=True).items():
        setattr(kassa, name, value)

    await session.commit()
    return kassa
