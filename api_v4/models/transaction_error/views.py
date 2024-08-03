from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import TrErrorCreate, TrError
from .dependencies import error_by_id
from . import crud

router = APIRouter(tags=["TransactionErrors"])


@router.get("/", response_model=List[TrError])
async def get_errors(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_errors(session=session)


@router.post("/", response_model=TrError, status_code=status.HTTP_201_CREATED)
async def create_error(
    error_in: TrErrorCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    error = await crud.create_error(session=session, error_in=error_in)
    return error


@router.get("/{error_id}/", response_model=TrError)
async def get_error(error: TrError = Depends(error_by_id)):
    return error
