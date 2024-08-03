from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Client, ClientCreate, ClientUpdate, ClientAuth
from .dependencies import client_by_id
from . import crud
from .auth import auth


router = APIRouter(tags=["Clients"])


@router.get("/", response_model=List[Client])
async def get_clients(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_clients(session=session)


@router.post("/", response_model=Client, status_code=status.HTTP_201_CREATED)
async def create_client(
    client_in: ClientCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    client = await crud.create_client(session=session, client_in=client_in)
    return client


@router.get("/{client_id}/", response_model=Client)
async def get_client(client: Client = Depends(client_by_id)):
    return client


@router.patch("/{client_id}/", response_model=Client)
async def update_client(
    client_update: ClientUpdate,
    client: Client = Depends(client_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_client(
        client_update=client_update,
        client=client,
        session=session,
    )


@router.post("/auth/")
async def client_auth(
    client: ClientAuth,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await auth(
        session=session,
        client_data=client,
    )
