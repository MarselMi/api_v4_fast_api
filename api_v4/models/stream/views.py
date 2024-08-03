from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Stream, StreamCreate, StreamUpdate
from .dependencies import stream_by_id
from . import crud

router = APIRouter(tags=["Streams"])


@router.get("/", response_model=List[Stream])
async def get_streams(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_streams(session=session)


@router.post("/", response_model=Stream, status_code=status.HTTP_201_CREATED)
async def create_stream(
    stream_in: StreamCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    stream = await crud.create_stream(session=session, stream_in=stream_in)
    return stream


@router.get("/{stream_id}/", response_model=Stream)
async def get_stream(stream: Stream = Depends(stream_by_id)):
    return stream


@router.patch("/{stream_id}/", response_model=Stream)
async def update_stream(
    stream_in: StreamUpdate,
    stream: Stream = Depends(stream_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_stream(
        session=session,
        stream=stream,
        stream_in=stream_in,
    )
