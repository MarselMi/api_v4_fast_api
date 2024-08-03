from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from . import crud
from .schemas import Host, HostCreate, HostUpdate
from .dependencies import host_by_id

router = APIRouter(tags=["Hosts"])


@router.get("/", response_model=List[Host])
async def get_host(
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_hosts(session=session)


@router.post("/", response_model=Host, status_code=status.HTTP_201_CREATED)
async def create_host(
        host_in: HostCreate,
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    host = await crud.create_host(session=session, host_in=host_in)
    return host


@router.get("/{host_id}/", response_model=Host)
async def get_host(host: Host = Depends(host_by_id)):
    return host


@router.patch("/{host_id}/", response_model=Host)
async def update_host(
        host_update: HostUpdate,
        host: Host = Depends(host_by_id),
        session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_host(
        session=session,
        host=host,
        host_update=host_update,
    )
