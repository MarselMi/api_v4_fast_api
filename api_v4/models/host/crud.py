from core.models import Host
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import HostCreate, HostUpdate

from core.models import Stream

from api_v4.models.stream.dependencies import stream_by_id
from api_v4.models.partner.dependencies import partner_by_id
from api_v4.models.landing.dependencies import landing_by_id
from api_v4.models.manager.dependencies import manager_by_id
from api_v4.models.offer.dependencies import offer_by_id


async def get_hosts(session: AsyncSession) -> List[Host]:
    query = select(Host).order_by(Host.id)
    result: Result = await session.execute(query)
    hosts = result.scalars().all()
    return list(hosts)


async def get_host(session: AsyncSession, host_id: int) -> Host | None:
    return await session.get(Host, host_id)


async def create_host(session: AsyncSession, host_in: HostCreate) -> Host:
    await landing_by_id(landing_id=host_in.landing_id, session=session)
    host_in.n_landing_id = host_in.landing_id

    await stream_by_id(stream_id=host_in.stream_id, session=session)
    host_in.n_stream_id = host_in.stream_id

    query = select(Stream).filter(Stream.id == host_in.stream_id)
    stream: Stream = await session.scalar(query)
    await offer_by_id(offer_id=stream.offer_id, session=session)
    host_in.n_offer_id = stream.offer_id

    await partner_by_id(partner_id=host_in.partner_id, session=session)
    host_in.n_partner_id = host_in.partner_id

    if host_in.manager_id:
        await manager_by_id(manager_id=host_in.manager_id, session=session)
        host_in.n_manager_id = host_in.manager_id

    host = Host(**host_in.model_dump())
    session.add(host)
    await session.commit()
    return host


async def update_host(session: AsyncSession, host: Host, host_update: HostUpdate):
    for name, value in host_update.model_dump(exclude_unset=True).items():
        setattr(host, name, value)
    await session.commit()
    return host
