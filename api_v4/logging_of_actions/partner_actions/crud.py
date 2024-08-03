from core.models import PartnerAction
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import CreatePartnerAction


async def get_actions(
    session: AsyncSession,
) -> List[PartnerAction]:
    query = select(PartnerAction).order_by(PartnerAction.id)
    result: Result = await session.execute(query)
    actions = result.scalars().all()
    return list(actions)


async def get_action(
    session: AsyncSession,
    action_id: int,
) -> PartnerAction | None:
    return await session.get(PartnerAction, action_id)


async def create_action(
    session: AsyncSession,
    action_in: CreatePartnerAction,
) -> PartnerAction:
    action_in = action_in.model_dump()
    action = PartnerAction(**action_in)
    session.add(action)
    await session.commit()
    return action
