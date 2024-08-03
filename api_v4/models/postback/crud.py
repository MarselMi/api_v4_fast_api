from sqlalchemy.orm import selectinload

from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.models import Postback, Partner, Manager
from core.models import Event

from .schemas import PostbackCreate, PostbackUpdate

from fastapi import HTTPException, status


async def get_postbacks(
    session: AsyncSession,
) -> List[Postback]:
    query = (
        select(Postback).options(selectinload(Postback.event_id)).order_by(Postback.id)
    )
    result: Result = await session.execute(query)
    postbacks = result.scalars().all()
    return list(postbacks)


async def get_postback(
    session: AsyncSession,
    postback_id: int,
) -> Postback | None:
    query = (
        select(Postback)
        .options(selectinload(Postback.event_id))
        .filter(Postback.id == postback_id)
    )
    result = await session.scalar(query)

    return result


async def create_postback(
    session: AsyncSession,
    postback_in: PostbackCreate,
) -> Postback:

    events_list = []
    if postback_in.event_id:
        for event_id in postback_in.event_id:
            query = select(Event).where(Event.id == event_id)
            event: Event = await session.scalar(query)
            if event is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"event с id {event_id} не найден",
                )
            else:
                events_list.append(event)

    if postback_in.partner_id:
        partner = await session.get(Partner, postback_in.partner_id)
        if partner is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"partner с id {postback_in.partner_id} не найден",
            )
    if postback_in.manager_id:
        manager = await session.get(Manager, postback_in.manager_id)
        if manager is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"manager с id {postback_in.manager_id} не найден",
            )

    postback_in.event_id = events_list

    postback = Postback(**postback_in.model_dump())

    session.add(postback)
    await session.commit()

    return postback


async def update_postback(
    session: AsyncSession,
    postback: Postback,
    postback_in: PostbackUpdate,
) -> Postback:

    if postback_in.event_id:
        events_list = []

        for event_id in postback_in.event_id:
            query = select(Event).where(Event.id == event_id)
            event: Event = await session.scalar(query)
            events_list.append(event)

        postback_in.event_id = events_list

    for name, value in postback_in.model_dump(exclude_unset=True).items():
        setattr(postback, name, value)

    # session.add(postback)
    await session.commit()
    return postback
