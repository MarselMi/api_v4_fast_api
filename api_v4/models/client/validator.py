from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from .schemas import ClientUpdate, ClientCreate

from core.models import Client, Offer

from sqlalchemy import select
from sqlalchemy.engine import Result


class ClientValidator:

    async def validate(
        self,
        client: ClientCreate | ClientUpdate,
        session: AsyncSession,
    ):
        if isinstance(client, ClientCreate):
            await self.check_phone_email(
                email=client.email,
                phone=client.phone,
            )

            await self.validate_unique(
                email=client.email,
                phone=client.phone,
                offer_id=client.offer_id,
                session=session,
            )

    @staticmethod
    async def check_phone_email(email: str | None, phone: str | None):
        if email is None and phone is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Одно из полей email / phone должно быть заполнено",
            )

    @staticmethod
    async def validate_unique(
        email: str | None,
        phone: str | None,
        offer_id: int | None,
        session: AsyncSession,
    ):
        if offer_id is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Не передан офер",
            )
        if email:
            query = (
                select(Client)
                .where(Client.email == email)
                .where(Client.offer_id == offer_id)
            )
        else:
            query = (
                select(Client)
                .where(Client.phone == phone)
                .where(Client.offer_id == offer_id)
            )

        result: Result = await session.execute(query)
        client: list[Client] = result.scalars().all()

        if len(client) > 0:
            offer: Offer | None = await session.get(Offer, offer_id)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Ошибка уникальности: {client[0].email if client[0].email else client[0].phone} offer: {offer.name}",
            )
