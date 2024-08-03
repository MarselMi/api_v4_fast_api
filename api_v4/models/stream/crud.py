from random import randint

from core.models import (
    Stream,
    Postback,
    Offer,
    Landing,
    Prelanding,
    Manager,
    Partner,
    LandingElement,
)
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from fastapi import HTTPException, status

from .schemas import StreamCreate, StreamUpdate
from .functions import BASE62, decode, encode, DOMAIN


async def get_streams(
    session: AsyncSession,
) -> List[Stream]:
    query = select(Stream).options(selectinload(Stream.postback_id)).order_by(Stream.id)

    result: Result = await session.execute(query)
    streams = result.scalars().all()
    return list(streams)


async def get_stream(
    session: AsyncSession,
    stream_id: int,
) -> Stream | None:
    query = (
        select(Stream)
        .options(selectinload(Stream.postback_id))
        .filter(Stream.id == stream_id)
    )

    result = await session.scalar(query)

    return result


async def create_stream(
    session: AsyncSession,
    stream_in: StreamCreate,
) -> Stream:

    postbacks_list = []
    if stream_in.postback_id:
        for postback_id in stream_in.postback_id:
            query = select(Postback).where(Postback.id == postback_id)
            postback: Postback = await session.scalar(query)
            if postback is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"postback с id {postback_id} не найден",
                )
            else:
                postbacks_list.append(postback)

    offer = await session.get(Offer, stream_in.offer_id)
    if offer is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"offer с id {stream_in.offer_id} не найден",
        )

    landing = await session.get(Landing, stream_in.landing_id)
    if landing is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"landing с id {stream_in.landing_id} не найден",
        )

    # if landing.landing_elements:
    #     landing_element = await session.get(LandingElement, landing.landing_elements)
    #     stream_in.landingelement_data = landing_element.elements

    if stream_in.prelanding_id:
        prelanding = await session.get(Prelanding, stream_in.prelanding_id)
        if prelanding is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"prelanding с id {stream_in.prelanding_id} не найден",
            )
    if stream_in.manager_id:
        manager = await session.get(Manager, stream_in.manager_id)
        if manager is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"manager с id {stream_in.manager_id} не найден",
            )

    partner = await session.get(Partner, stream_in.partner_id)
    if partner is None:
        raise HTTPException(
            status_code=status.HTTP_424_FAILED_DEPENDENCY,
            detail=f"partner с id {stream_in.partner_id} не найден",
        )

    uid = randint(0, 1000000000)
    stream_in.uid = uid
    stream_in.link = f"{DOMAIN}{await encode(num=uid, alphabet=BASE62)}"
    stream_in.postback_id = postbacks_list

    stream = Stream(**stream_in.model_dump())

    session.add(stream)
    await session.commit()

    return stream


async def update_stream(
    session: AsyncSession,
    stream: Stream,
    stream_in: StreamUpdate,
) -> Stream:

    if stream_in.postback_id:
        postbacks_list = []

        for postback_id in stream_in.postback_id:
            postback = await session.get(Postback, postback_id)
            if postback is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"postback с id {postback_id} не найден",
                )
            else:
                postbacks_list.append(postback)

        stream_in.postback_id = postbacks_list

    for name, value in stream_in.model_dump(exclude_unset=True).items():
        setattr(stream, name, value)

    await session.commit()
    return stream
