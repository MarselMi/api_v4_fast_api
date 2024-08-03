from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from core.models import db_helper
from .schemas import Organisation, OrganisationCreate
from .dependencies import organisation_by_id
from . import crud

router = APIRouter(tags=["Organisations"])


@router.get("/", response_model=List[Organisation])
async def get_organisations(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_organisations(session=session)


@router.post("/", response_model=Organisation, status_code=status.HTTP_201_CREATED)
async def create_organisation(
    organisation_in: OrganisationCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    organisation_in = await crud.create_organisation(
        session=session, organisation_in=organisation_in
    )
    return organisation_in


@router.get("/{organisation_id}/", response_model=Organisation)
async def get_organisation(organisation: Organisation = Depends(organisation_by_id)):
    return organisation
