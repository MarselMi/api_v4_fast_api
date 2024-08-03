from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Event, EventCreate
from .dependencies import event_by_id
from . import crud

router = APIRouter(tags=["Events"])


@router.get("/", response_model=List[Event])
async def get_events(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_events(session=session)


@router.post("/", response_model=Event, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_in: EventCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    event = await crud.create_event(session=session, event_in=event_in)
    return event


@router.get("/{event_id}/", response_model=Event)
async def get_event(event: Event = Depends(event_by_id)):
    return event
