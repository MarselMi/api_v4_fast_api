from core.models import Terminal, Organisation, Offer, Paysystem, Kassa, AcquBank
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from fastapi import status, HTTPException

from .schemas import TerminalCreate, TerminalUpdate


async def get_terminals(
    session: AsyncSession,
) -> List[Terminal]:
    query = select(Terminal).order_by(Terminal.id)
    result: Result = await session.execute(query)
    res = result.scalars().all()
    return list(res)


async def get_terminal(
    session: AsyncSession,
    terminal_id: int,
) -> Terminal | None:
    return await session.get(Terminal, terminal_id)


async def create_terminal(
    session: AsyncSession,
    terminal_in: TerminalCreate,
) -> Terminal:

    if terminal_in.organisation_id:
        res = await session.get(Organisation, terminal_in.organisation_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"organisation с id {terminal_in.organisation_id} не найден",
            )
    if terminal_in.offer_id:
        res = await session.get(Offer, terminal_in.offer_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"offer с id {terminal_in.offer_id} не найден",
            )
    if terminal_in.paysystem_id:
        res = await session.get(Paysystem, terminal_in.paysystem_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"paysystem с id {terminal_in.paysystem_id} не найден",
            )
    if terminal_in.kassa_id:
        res = await session.get(Kassa, terminal_in.kassa_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"kassa с id {terminal_in.kassa_id} не найден",
            )
    if terminal_in.acqu_bank:
        res = await session.get(AcquBank, terminal_in.acqu_bank)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"acqu_bank с id {terminal_in.acqu_bank} не найден",
            )

    obj = Terminal(**terminal_in.model_dump())
    session.add(obj)
    await session.commit()
    return obj


async def update_terminal(
    session: AsyncSession,
    terminal: Terminal,
    terminal_update: TerminalUpdate,
) -> Terminal:

    if terminal_update.organisation_id:
        res = await session.get(Organisation, terminal_update.organisation_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"organisation с id {terminal_update.organisation_id} не найден",
            )
    if terminal_update.offer_id:
        res = await session.get(Offer, terminal_update.offer_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"offer с id {terminal_update.offer_id} не найден",
            )
    if terminal_update.paysystem_id:
        res = await session.get(Paysystem, terminal_update.paysystem_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"paysystem с id {terminal_update.paysystem_id} не найден",
            )
    if terminal_update.kassa_id:
        res = await session.get(Kassa, terminal_update.kassa_id)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"kassa с id {terminal_update.kassa_id} не найден",
            )
    if terminal_update.acqu_bank:
        res = await session.get(AcquBank, terminal_update.acqu_bank)
        if res is None:
            raise HTTPException(
                status_code=status.HTTP_424_FAILED_DEPENDENCY,
                detail=f"acqu_bank с id {terminal_update.acqu_bank} не найден",
            )

    for name, value in terminal_update.model_dump(exclude_unset=True).items():
        setattr(terminal, name, value)

    await session.commit()
    return terminal
