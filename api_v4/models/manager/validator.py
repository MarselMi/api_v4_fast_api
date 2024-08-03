from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api_v4.models.manager.schemas import ManagerCreate, ManagerUpdate
from core.models import Manager
from sqlalchemy import select
from sqlalchemy.engine import Result


class ManagerValidator:

    async def validate(
        self,
        manager: ManagerCreate | ManagerUpdate,
        session: AsyncSession,
    ):
        if isinstance(manager, ManagerCreate):
            await self.validate_unique_email(manager.email, session)

    @staticmethod
    async def validate_unique_email(email: str, session: AsyncSession):
        query = select(Manager.email).where(Manager.email == email)
        result: Result = await session.execute(query)
        manager = result.scalars().all()
        if len(manager) > 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="manager с таким email уже зарегистрирован",
            )
