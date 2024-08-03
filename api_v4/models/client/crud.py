from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import status, HTTPException

from typing import List
import uuid as uuid_gen

from .schemas import ClientCreate, ClientUpdate
from .validator import ClientValidator
from api_v4.models.offer.dependencies import offer_by_id

from core.hasher import PasswordHasher
from core.models import Client, Host, Stream
from api_v4.models.host.schemas import HostCreate


async def get_clients(session: AsyncSession) -> List[Client]:
    query = select(Client).order_by(Client.id)
    result: Result = await session.execute(query)
    res = result.scalars().all()
    return list(res)


async def get_client(session: AsyncSession, client_id: int) -> Client | None:
    return await session.get(Client, client_id)


async def create_client(
    session: AsyncSession,
    client_in: ClientCreate,
) -> Client:
    hasher = PasswordHasher()
    validator = ClientValidator()

    await validator.validate(client_in, session)

    client_in.password = hasher.encode(client_in.password, hasher.salt())

    await offer_by_id(offer_id=client_in.offer_id, session=session)

    if client_in.uuid:
        query = select(Host).filter(Host.uuid == client_in.uuid)
        host: Host = await session.scalar(query)
    else:
        client_in.uuid = uuid_gen.uuid4()
        host_data_create = HostCreate(
            uuid=client_in.uuid,
            n_offer_id=1,
            partner_id=1,
            stream_id=1,
            landing_id=1,
            n_partner_id=1,
            n_stream_id=1,
            n_landing_id=1,
        )
        host = Host(**host_data_create.model_dump())
        session.add(host)

        query = select(Host).filter(Host.uuid == client_in.uuid)
        host: Host = await session.scalar(query)

    host_id = host.id
    client_in.host_id = host_id
    client_in.n_host_id = host_id

    stream: Stream | None = await session.get(Stream, host.stream_id)
    if stream is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Поток не найден",
        )

    client_in.n_stream_id = host.stream_id
    client_in.n_offer_id = client_in.offer_id
    client_in.n_landing_id = host.landing_id
    client_in.n_partner_id = host.partner_id

    if host.manager_id:
        client_in.n_manager_id = host.manager_id

    client = Client(**client_in.model_dump())

    session.add(client)
    await session.commit()

    return client


async def update_client(
    session: AsyncSession,
    client_update: ClientUpdate,
    client: Client,
) -> Client:
    hasher = PasswordHasher()
    validator = ClientValidator()

    await validator.validate(client_update, session)
    for name, value in client_update.model_dump(exclude_unset=True).items():
        if name == "password":
            value = hasher.encode(value, hasher.salt())
        setattr(client, name, value)

    await session.commit()
    return client
