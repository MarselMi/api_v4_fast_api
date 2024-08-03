from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from api_v4.models.partner.schemas import PartnerCreate, PartnerUpdate
from core.models import Partner
from sqlalchemy import select
from sqlalchemy.engine import Result


class PartnerValidator:

    async def validate(self, partner: PartnerCreate | PartnerUpdate, session: AsyncSession):
        if isinstance(partner, PartnerCreate):
            await self.validate_unique_email(partner.email, session)
        await self.check_referal_field_is_not_zero(partner)
        await self.check_referal_exists(partner, session)

    @staticmethod
    async def validate_unique_email(email: str, session: AsyncSession):
        query = select(Partner.email).where(Partner.email == email)
        result: Result = await session.execute(query)
        partner = result.scalars().all()
        if len(partner) > 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Партнер с таким email уже зарегистрирован",
            )

    @staticmethod
    async def check_referal_field_is_not_zero(partner_in: PartnerCreate | PartnerUpdate):
        if partner_in.model_dump().get('referal') == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Поле referal должно быть больше нуля",
            )

    @staticmethod
    async def check_referal_exists(partner_in: PartnerCreate | PartnerUpdate, session: AsyncSession):
        referal_id = partner_in.model_dump().get('referal')
        if referal_id:
            query = select(Partner.email).where(Partner.id == referal_id)
            result: Result = await session.execute(query)
            partner = result.scalars().all()
            if len(partner) == 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Переданный id, в поле referal, не соответствует ни одному партнеру"
                )
