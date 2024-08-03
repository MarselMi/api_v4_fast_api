from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import LandingCreate, Landing, LandingUpdate, LandingRel
from .dependencies import landing_by_id
from . import crud


router = APIRouter(tags=["Landings"])


@router.get("/", response_model=List[Landing])
async def get_landings(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_landings(session=session)


@router.post("/", response_model=Landing, status_code=status.HTTP_201_CREATED)
async def create_landing(
    landing_in: LandingCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    landing = await crud.create_landing(session=session, landing_in=landing_in)
    return landing


@router.get("/{landing_id}/", response_model=LandingRel)
async def get_landing(landing: Landing = Depends(landing_by_id)):
    return landing


@router.patch("/{landing_id}/", response_model=Landing)
async def update_landing(
    landing_update: LandingUpdate,
    landing: Landing = Depends(landing_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_landing(
        session=session,
        landing=landing,
        landing_update=landing_update,
    )
