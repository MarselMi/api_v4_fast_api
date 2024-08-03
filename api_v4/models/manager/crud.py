from core.hasher import PasswordHasher

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from core.models import Manager
from core.models import Partner

from .schemas import ManagerCreate, ManagerUpdate
from .validator import ManagerValidator


async def get_managers(
    session: AsyncSession,
) -> List[Manager]:
    query = (
        select(Manager).options(selectinload(Manager.partners_id)).order_by(Manager.id)
    )
    result: Result = await session.execute(query)
    managers = result.scalars().all()

    return list(managers)


async def get_manager(
    session: AsyncSession,
    manager_id: int,
) -> Manager | None:
    query = (
        select(Manager)
        .options(selectinload(Manager.partners_id))
        .filter(Manager.id == manager_id)
    )
    result = await session.scalar(query)

    return result


async def create_manager(
    session: AsyncSession,
    manager_in: ManagerCreate,
) -> Manager:
    hasher = PasswordHasher()
    validator = ManagerValidator()

    await validator.validate(manager_in, session)

    manager_in.password = hasher.encode(manager_in.password, hasher.salt())

    partners_list = []
    if manager_in.partners_id:
        for partner_id in manager_in.partners_id:
            query = select(Partner).where(Partner.id == partner_id)
            partner: Partner = await session.scalar(query)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
    manager_in.partners_id = partners_list

    manager = Manager(**manager_in.model_dump())
    manager.partners_id = partners_list

    session.add(manager)
    await session.commit()

    return manager


async def update_manager(
    session: AsyncSession,
    manager: Manager,
    manager_update: ManagerUpdate,
) -> Manager:
    hasher = PasswordHasher()
    validator = ManagerValidator()

    if manager_update.partners_id:
        partners_list = []
        for partner_id in manager_update.partners_id:
            query = select(Partner).where(Partner.id == partner_id)
            partner: Partner = await session.scalar(query)
            if partner is None:
                raise HTTPException(
                    status_code=status.HTTP_424_FAILED_DEPENDENCY,
                    detail=f"partner с id {partner_id} не найден",
                )
            else:
                partners_list.append(partner)
        manager_update.partners_id = partners_list

    await validator.validate(manager_update, session)
    for name, value in manager_update.model_dump(exclude_unset=True).items():
        if name == "password":
            value = hasher.encode(value, hasher.salt())
        setattr(manager, name, value)
    await session.commit()
    return manager
