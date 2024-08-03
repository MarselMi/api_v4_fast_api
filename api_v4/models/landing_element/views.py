from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import LandingElement, LandingElementCreate, LandingElementUpdate
from .dependencies import land_element_by_id
from . import crud

router = APIRouter(tags=["LandingElements"])


@router.get("/", response_model=List[LandingElement])
async def get_land_elements(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_land_elements(session=session)


@router.post("/", response_model=LandingElement, status_code=status.HTTP_201_CREATED)
async def create_land_element(
    land_element_in: LandingElementCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    land_element = await crud.create_land_element(
        session=session, land_element_in=land_element_in
    )
    return land_element


@router.get("/{land_element_id}/", response_model=LandingElement)
async def get_land_element(land_element: LandingElement = Depends(land_element_by_id)):
    return land_element


@router.patch("/{land_element_id}/", response_model=LandingElement)
async def update_land_element(
    land_element_in: LandingElementUpdate,
    land_element: LandingElement = Depends(land_element_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_land_element(
        session=session,
        land_element_in=land_element_in,
        land_element=land_element,
    )
