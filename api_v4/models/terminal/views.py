from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import TerminalCreate, Terminal, TerminalUpdate
from .dependencies import terminal_by_id
from . import crud

router = APIRouter(tags=["Terminals"])


@router.get("/", response_model=List[Terminal])
async def get_terminals(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_terminals(session=session)


@router.post("/", response_model=Terminal, status_code=status.HTTP_201_CREATED)
async def create_error(
    terminal_in: TerminalCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    terminal = await crud.create_terminal(session=session, terminal_in=terminal_in)
    return terminal


@router.get("/{terminal_id}/", response_model=Terminal)
async def get_terminal(terminal: Terminal = Depends(terminal_by_id)):
    return terminal


@router.patch("/{terminal_id}/", response_model=Terminal)
async def update_terminal(
    terminal_update: TerminalUpdate,
    terminal: Terminal = Depends(terminal_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_terminal(
        session=session,
        terminal_update=terminal_update,
        terminal=terminal,
    )
