from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import AcquBank, AcquBankCreate
from .dependencies import acqu_bank_by_id
from . import crud

router = APIRouter(tags=["AcquBanks"])


@router.get("/", response_model=List[AcquBank])
async def get_land_elements(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_acqu_banks(session=session)


@router.post("/", response_model=AcquBank, status_code=status.HTTP_201_CREATED)
async def create_acqu_bank(
    acqu_bank_in: AcquBankCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    acqu_bank = await crud.create_acqu_bank(session=session, acqu_bank_in=acqu_bank_in)
    return acqu_bank


@router.get("/{acqu_bank_id}/", response_model=AcquBank)
async def get_acqu_bank(acqu_bank: AcquBank = Depends(acqu_bank_by_id)):
    return acqu_bank
