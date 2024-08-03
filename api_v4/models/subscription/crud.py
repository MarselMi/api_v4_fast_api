from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import status, HTTPException

from typing import List

from .schemas import SubscriptionCreate, SubscriptionUpdate

from api_v4.models.offer.dependencies import offer_by_id
from api_v4.models.client.dependencies import client_by_id
from api_v4.models.partner.dependencies import partner_by_id
from api_v4.models.partner.dependencies import partner_by_id
from api_v4.models.partner.dependencies import partner_by_id
from api_v4.models.terminal.dependencies import terminal_by_id

from core.models import Client, Host, Stream, Subscription, Offer


async def get_subscriptions(
    session: AsyncSession,
) -> List[Subscription]:
    query = select(Subscription).order_by(Subscription.id)
    result: Result = await session.execute(query)
    res = result.scalars().all()
    return list(res)


async def get_subscription(
    session: AsyncSession,
    subscription_id: int,
) -> Subscription | None:
    return await session.get(Subscription, subscription_id)


async def create_subscription(
    session: AsyncSession,
    subscription_in: SubscriptionCreate,
) -> Subscription:

    # await offer_by_id(offer_id=client_in.offer_id, session=session)

    # host_id = host.id
    # client_in.host_id = host_id
    # client_in.n_host_id = host_id
    #
    # stream: Stream | None = await session.get(Stream, host.stream_id)
    # if stream is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #         detail=f"Поток не найден",
    #     )
    #
    # client_in.n_stream_id = host.stream_id
    # client_in.n_offer_id = client_in.offer_id
    # client_in.n_landing_id = host.landing_id
    # client_in.n_partner_id = host.partner_id
    #
    # if host.manager_id:
    #     client_in.n_manager_id = host.manager_id

    if subscription_in.terminal_id:
        await terminal_by_id(terminal_id=subscription_in.terminal_id, session=session)

    subscription = Subscription(**subscription_in.model_dump())

    session.add(subscription)
    await session.commit()

    return subscription


async def update_subscription(
    session: AsyncSession,
    subscription_update: SubscriptionUpdate,
    subscription: Subscription,
) -> Subscription:

    for name, value in subscription_update.model_dump(exclude_unset=True).items():
        setattr(subscription, name, value)

    await session.commit()
    return subscription
