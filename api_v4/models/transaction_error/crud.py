from core.models import TransactionError
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import TrErrorCreate


async def get_errors(
    session: AsyncSession,
) -> List[TransactionError]:
    query = select(TransactionError).order_by(TransactionError.id)
    result: Result = await session.execute(query)
    event = result.scalars().all()
    return list(event)


async def get_error(
    session: AsyncSession,
    error_id: int,
) -> TransactionError | None:
    return await session.get(TransactionError, error_id)


async def create_error(
    session: AsyncSession,
    error_in: TrErrorCreate,
) -> TransactionError:

    obj = TransactionError(**error_in.model_dump())
    session.add(obj)
    await session.commit()
    return obj
