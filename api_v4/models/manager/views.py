from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper

from . import crud
from .schemas import Manager, ManagerCreate, ManagerUpdate
from .dependencies import manager_by_id

router = APIRouter(tags=["Managers"])


@router.get("/", response_model=List[Manager])
async def get_managers(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_managers(session=session)


@router.post("/", response_model=Manager, status_code=status.HTTP_201_CREATED)
async def create_partner(
    manager_in: ManagerCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    manager = await crud.create_manager(session=session, manager_in=manager_in)
    return manager


@router.get("/{manager_id}/", response_model=Manager)
async def get_manager(manager: Manager = Depends(manager_by_id)):
    return manager


@router.patch("/{manager_id}/", response_model=Manager)
async def update_partner(
    manager_update: ManagerUpdate,
    manager: Manager = Depends(manager_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_manager(
        session=session,
        manager=manager,
        manager_update=manager_update,
    )
