from core.models import OperatorAction
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import CreateOperatorAction


async def get_actions(
    session: AsyncSession,
) -> List[OperatorAction]:
    query = select(OperatorAction).order_by(OperatorAction.id)
    result: Result = await session.execute(query)
    actions = result.scalars().all()
    return list(actions)


async def get_action(
    session: AsyncSession,
    action_id: int,
) -> OperatorAction | None:
    return await session.get(OperatorAction, action_id)


async def create_action(
    session: AsyncSession,
    action_in: CreateOperatorAction,
) -> OperatorAction:
    action_in = action_in.model_dump()
    action = OperatorAction(**action_in)
    session.add(action)
    await session.commit()
    return action
