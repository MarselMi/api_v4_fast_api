from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Kassa, KassaCreate, KassaRel, KassaUpdate
from .dependencies import kassa_by_id
from . import crud

router = APIRouter(tags=["Kasses"])


@router.get("/", response_model=List[Kassa])
async def get_kasses(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_kasses(session=session)


@router.post("/", response_model=Kassa, status_code=status.HTTP_201_CREATED)
async def create_kassa(
    kassa_in: KassaCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    kassa_in = await crud.create_kassa(session=session, kassa_in=kassa_in)
    return kassa_in


@router.get("/{kassa_id}/", response_model=KassaRel)
async def get_kassa(kassa: KassaRel = Depends(kassa_by_id)):
    return kassa


@router.patch("/{kassa_id}/", response_model=Kassa)
async def update_stream(
    kassa_update: KassaUpdate,
    kassa: Kassa = Depends(kassa_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_kassa(
        session=session,
        kassa=kassa,
        kassa_update=kassa_update,
    )
