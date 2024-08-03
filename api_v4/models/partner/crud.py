from core.hasher import PasswordHasher
from core.models import Partner
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .schemas import PartnerCreate, PartnerUpdate
from .utils import generate_partner_uid
from .validator import PartnerValidator


async def get_partners(session: AsyncSession) -> List[Partner]:
    query = select(Partner).order_by(Partner.id)
    result: Result = await session.execute(query)
    partners = result.scalars().all()
    return list(partners)


async def get_partner(session: AsyncSession, partner_id: int) -> Partner | None:
    return await session.get(Partner, partner_id)


async def create_partner(session: AsyncSession, partner_in: PartnerCreate) -> Partner:
    hasher = PasswordHasher()
    validator = PartnerValidator()

    await validator.validate(partner_in, session)

    partner_in.password = hasher.encode(partner_in.password, hasher.salt())

    partner = Partner(**partner_in.model_dump())
    session.add(partner)
    await session.commit()

    partner = await generate_partner_uid(partner_id=partner.id, session=session)

    return partner


async def update_partner(
        session: AsyncSession,
        partner: Partner,
        partner_update: PartnerUpdate
):
    hasher = PasswordHasher()
    validator = PartnerValidator()

    await validator.validate(partner_update, session)
    for name, value in partner_update.model_dump(exclude_unset=True).items():
        if name == 'password':
            value = hasher.encode(value, hasher.salt())
        setattr(partner, name, value)
    await session.commit()
    return partner
