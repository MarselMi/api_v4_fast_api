from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.models import db_helper
from core.models import OperatorAction
from api_v4.logging_of_actions.operator_actions import crud
from api_v4.logging_of_actions.operator_actions.schemas import CreateOperatorAction
from api_v4.logging_of_actions.operator_actions.dependencies import action_by_id


router = APIRouter(tags=["OperatorAction"])


@router.post("/", response_model=OperatorAction, status_code=status.HTTP_201_CREATED)
async def create_operator_action(
    action_in: CreateOperatorAction,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_action(session=session, action_in=action_in)


@router.get("/{action_id}/", response_model=OperatorAction)
async def get_action(
    action: OperatorAction = Depends(action_by_id),
):
    return action


@router.get("/", response_model=List[OperatorAction])
async def get_operator_actions(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_actions(session=session)
