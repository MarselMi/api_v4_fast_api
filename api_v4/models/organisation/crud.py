from core.models import Organisation
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import OrganisationCreate


async def get_organisations(session: AsyncSession) -> List[Organisation]:
    query = select(Organisation).order_by(Organisation.id)
    result: Result = await session.execute(query)
    organisations = result.scalars().all()
    return list(organisations)


async def get_organisation(
    session: AsyncSession, organisation_id: int
) -> Organisation | None:
    return await session.get(Organisation, organisation_id)


async def create_organisation(
    session: AsyncSession, organisation_in: OrganisationCreate
) -> Organisation:
    organisation_in = organisation_in.model_dump()
    organisation = Organisation(**organisation_in)
    session.add(organisation)
    await session.commit()
    return organisation
