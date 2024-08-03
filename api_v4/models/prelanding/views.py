from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import PrelandingCreate, Prelanding, PrelandingUpdate
from .dependencies import prelanding_by_id
from . import crud


router = APIRouter(tags=["Prelandings"])


@router.get("/", response_model=List[Prelanding])
async def get_prelandings(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_prelandings(session=session)


@router.post("/", response_model=Prelanding, status_code=status.HTTP_201_CREATED)
async def create_prelanding(
    prelanding_in: PrelandingCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    prelanding = await crud.create_prelanding(
        session=session, prelanding_in=prelanding_in
    )
    return prelanding


@router.get("/{prelanding_id}/", response_model=Prelanding)
async def get_prelanding(prelanding: Prelanding = Depends(prelanding_by_id)):
    return prelanding


@router.patch("/{prelanding_id}/", response_model=Prelanding)
async def update_prelanding(
    prelanding_update: PrelandingUpdate,
    prelanding: Prelanding = Depends(prelanding_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_prelanding(
        session=session,
        prelanding=prelanding,
        prelanding_update=prelanding_update,
    )
