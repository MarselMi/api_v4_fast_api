from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import status, HTTPException

from .schemas import ClientAuth

from core.hasher import PasswordHasher
from core.models import Client


async def auth(
    session: AsyncSession,
    client_data: ClientAuth,
):
    if client_data.email is None and client_data.phone is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Введите email или телефон",
        )

    if client_data.password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Введите пароль",
        )

    if client_data.email:
        user_query = select(Client).where(
            and_(
                Client.email == client_data.email,
                # Client.password==password,
                Client.offer_id == client_data.offer_id,
            )
        )
        user = await session.scalar(user_query)
    else:
        user_query = select(Client).where(
            and_(
                Client.phone == client_data.phone,
                # Client.password==password,
                Client.offer_id == client_data.offer_id,
            )
        )
        user = await session.scalar(user_query)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь не зарегистрирован",
        )
    decoder = PasswordHasher()

    if client_data.password is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Введите пароль",
        )
    check = decoder.verify(password=client_data.password, encoded=user.password)
    if check:
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Неверный пароль",
        )
