from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Postback, PostbackCreate, PostbackUpdate
from .dependencies import postback_by_id
from . import crud

router = APIRouter(tags=["Postbacks"])


@router.get("/", response_model=List[Postback])
async def get_postbacks(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_postbacks(session=session)


@router.post("/", response_model=Postback, status_code=status.HTTP_201_CREATED)
async def create_postback(
    postback_in: PostbackCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    postback = await crud.create_postback(session=session, postback_in=postback_in)
    return postback


@router.get("/{postback_id}/", response_model=Postback)
async def get_postback(postback: Postback = Depends(postback_by_id)):
    return postback


@router.patch("/{postback_id}/", response_model=Postback)
async def update_postback(
    postback_in: PostbackUpdate,
    postback: Postback = Depends(postback_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> Postback:
    return await crud.update_postback(
        session=session, postback=postback, postback_in=postback_in
    )
