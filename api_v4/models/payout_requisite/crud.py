from core.models import PayoutRequisite
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import PaySystemUpdate, PayoutRequisite


async def get_payoutreqs(
    session: AsyncSession,
) -> List[PayoutRequisite]:
    query = select(PayoutRequisite).order_by(PayoutRequisite.id)
    result: Result = await session.execute(query)
    pay_reqs = result.scalars().all()
    return list(pay_reqs)


async def get_payoutreq(
    session: AsyncSession,
    payoutreq_id: int,
) -> PayoutRequisite | None:
    return await session.get(PayoutRequisite, payoutreq_id)


async def update_payoutreq(
    session: AsyncSession,
    pay_req_in: PaySystemUpdate,
    pay_req: PayoutRequisite,
) -> PayoutRequisite:

    for name, value in pay_req_in.model_dump(exclude_unset=True).items():
        setattr(pay_req, name, value)

    await session.commit()
    return pay_req
