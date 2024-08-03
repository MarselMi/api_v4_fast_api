from core.models import LandingElement
from sqlalchemy.engine import Result
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import LandingElementCreate, LandingElementUpdate


async def get_land_elements(session: AsyncSession) -> List[LandingElement]:
    query = select(LandingElement).order_by(LandingElement.id)
    result: Result = await session.execute(query)
    land_elements = result.scalars().all()
    return list(land_elements)


async def get_land_element(
    session: AsyncSession, land_element_id: int
) -> LandingElement | None:
    return await session.get(LandingElement, land_element_id)


async def create_land_element(
    session: AsyncSession, land_element_in: LandingElementCreate
) -> LandingElement:
    land_element_in = land_element_in.model_dump()
    land_element = LandingElement(**land_element_in)
    session.add(land_element)
    await session.commit()
    return land_element


async def update_land_element(
    session: AsyncSession,
    land_element_in: LandingElementUpdate,
    land_element: LandingElement,
):
    land_element.elements = str(land_element_in.elements)
    await session.commit()
    return land_element
