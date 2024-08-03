from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import KassType, KassTypeCreate
from .dependencies import kass_type_by_id
from . import crud

router = APIRouter(tags=["KassTypes"])


@router.get("/", response_model=List[KassType])
async def get_kass_types(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_kass_types(session=session)


@router.post("/", response_model=KassType, status_code=status.HTTP_201_CREATED)
async def create_kass_type(
    kass_type_in: KassTypeCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    kass_type = await crud.create_kass_type(session=session, kass_type_in=kass_type_in)
    return kass_type


@router.get("/{kass_type_id}/", response_model=KassType)
async def get_kass_type(kass_type: KassType = Depends(kass_type_by_id)):
    return kass_type
