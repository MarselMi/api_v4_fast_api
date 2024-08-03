from core.models import Event
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import EventCreate


async def get_events(session: AsyncSession) -> List[Event]:
    query = select(Event).order_by(Event.id)
    result: Result = await session.execute(query)
    event = result.scalars().all()
    return list(event)


async def get_event(session: AsyncSession, event_id: int) -> Event | None:
    return await session.get(Event, event_id)


async def create_event(session: AsyncSession, event_in: EventCreate) -> Event:
    event_in = event_in.model_dump()
    event = Event(**event_in)
    session.add(event)
    await session.commit()
    return event
