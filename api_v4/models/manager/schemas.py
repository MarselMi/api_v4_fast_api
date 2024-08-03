from typing import Optional, Annotated
from api_v4.models.partner.schemas import PartnerMin
from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime, date

from core.models.manager import RoleManagerChoices


class ManagerBase(BaseModel):
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr] = None
    phone: Annotated[str, MinLen(10), MaxLen(17)] | None = None
    name: Annotated[str, MinLen(2), MaxLen(60)] | None = None
    avatar: str | None = None
    telegram: str | None = None
    telegram_id: Annotated[int, Field(gt=0)] | None = None
    percent: Annotated[float, Field(ge=0)] | None = None
    user_is_active: bool = True
    role: Annotated[str, Optional[RoleManagerChoices]] | None = None
    email_verified: Annotated[int, Field(ge=0)] | None = None
    can_edit_offers: Annotated[int, Field(ge=0)] | None = None
    can_pay: Annotated[int, Field(ge=0)] | None = None
    partners_id: list["PartnerMin"] | None = None

    create_date: datetime | None = None
    create_date_day: date | None = None
    create_date_hour: Annotated[int, Field(ge=0)] | None = None
    change_date: datetime | None = None
    change_date_day: date | None = None
    change_date_hour: Annotated[int, Field(ge=0)] | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class ManagerCreate(ManagerBase):
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr]
    password: Annotated[str, MinLen(6), MaxLen(200)]
    partners_id: list[Annotated[int, Field(gt=0)]] | None = None


class ManagerUpdate(ManagerBase):
    partners_id: list[Annotated[int, Field(gt=0)]] | None = None
    password: Annotated[str, MinLen(6), MaxLen(200)] | None = None


class Manager(ManagerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ManagerForeign(Manager):
    partners_id: list["PartnerMin"] | None


class ManagerMin(BaseModel):
    id: int
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr]
