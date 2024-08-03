from core.models import AcquBank
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import AcquBankCreate


async def get_acqu_banks(session: AsyncSession) -> List[AcquBank]:
    query = select(AcquBank).order_by(AcquBank.id)
    result: Result = await session.execute(query)
    acqu_banks = result.scalars().all()
    return list(acqu_banks)


async def get_acqu_bank(session: AsyncSession, acqu_bank_id: int) -> AcquBank | None:
    return await session.get(AcquBank, acqu_bank_id)


async def create_acqu_bank(
    session: AsyncSession, acqu_bank_in: AcquBankCreate
) -> AcquBank:
    acqu_bank_in = acqu_bank_in.model_dump()
    acqu_bank = AcquBank(**acqu_bank_in)
    session.add(acqu_bank)
    await session.commit()
    return acqu_bank
