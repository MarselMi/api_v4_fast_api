from core.models import ManagerAction
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import CreateManagerAction


async def get_actions(
    session: AsyncSession,
) -> List[ManagerAction]:
    query = select(ManagerAction).order_by(ManagerAction.id)
    result: Result = await session.execute(query)
    actions = result.scalars().all()
    return list(actions)


async def get_action(
    session: AsyncSession,
    action_id: int,
) -> ManagerAction | None:
    return await session.get(ManagerAction, action_id)


async def create_action(
    session: AsyncSession,
    action_in: CreateManagerAction,
) -> ManagerAction:
    action_in = action_in.model_dump()
    action = ManagerAction(**action_in)
    session.add(action)
    await session.commit()
    return action
