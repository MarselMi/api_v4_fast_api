from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.models import db_helper
from core.models import ManagerAction
from api_v4.logging_of_actions.manager_actions import crud
from api_v4.logging_of_actions.manager_actions.dependencies import action_by_id
from api_v4.logging_of_actions.manager_actions.schemas import CreateManagerAction


router = APIRouter(tags=["ManagerActions"])


@router.post("/", response_model=ManagerAction, status_code=status.HTTP_201_CREATED)
async def create_partner_action(
    action_in: CreateManagerAction,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_action(session=session, action_in=action_in)


@router.get("/{action_id}/", response_model=ManagerAction)
async def get_action(
    action: ManagerAction = Depends(action_by_id),
):
    return action


@router.get("/", response_model=List[ManagerAction])
async def get_partner_actions(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_actions(session=session)
