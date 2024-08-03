from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import PaySystem, PaySystemCreate
from .dependencies import paysystem_by_id
from . import crud

router = APIRouter(tags=["PaySystem"])


@router.get("/", response_model=List[PaySystem])
async def get_paysystems(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_paysystems(session=session)


@router.post("/", response_model=PaySystem, status_code=status.HTTP_201_CREATED)
async def create_paysystem(
    paysystem_in: PaySystemCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    paysystem = await crud.create_paysystem(session=session, paysystem_in=paysystem_in)
    return paysystem


@router.get("/{paysystem_id}/", response_model=PaySystem)
async def get_paysystem(paysystem: PaySystem = Depends(paysystem_by_id)):
    return paysystem
