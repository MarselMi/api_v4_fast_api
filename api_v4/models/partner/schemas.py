from typing import Optional, Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime, date

from core.models.partner import ThemeChoices, RoleChoices


class PartnerBase(BaseModel):
    uid: str | None = None
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr] = None
    phone: Annotated[str, MinLen(10), MaxLen(17)] | None = None
    name: Annotated[str, MinLen(2), MaxLen(60)] | None = None
    avatar: str | None = None
    telegram: str | None = None
    telegram_id: Annotated[int, Field(ge=0)] | None = None
    percent: Annotated[float, Field(ge=0)] | None = None
    referal_fees: Annotated[float, Field(ge=0)] | None = None
    create_date: datetime | None = None
    create_date_day: date | None = None
    create_date_hour: Annotated[int, Field(ge=0)] | None = None
    last_activity: datetime | None = None
    ip_reg: str | None = None
    ip_auth: str | None = None
    referal: Annotated[int, Field(ge=0)] | None = None
    email_verified: Annotated[int, Field(ge=0)] | None = 0
    user_is_active: bool = True
    theme: Annotated[str, Optional[ThemeChoices]] | None = None
    role: Annotated[str, Optional[RoleChoices]] | None = None
    is_staff: bool | None = None
    is_superuser: bool | None = None
    want_to_get_notifications: bool | None = None
    contest_nick: Annotated[str, MinLen(1), MaxLen(20)] | None = None
    contest_check: bool = False
    two_factor_auth: Annotated[int, Field(ge=0)] | None = None
    traffic_is_stopped: Annotated[int, Field(ge=0)] | None = None
    comment: str | None = None
    permanent: Annotated[int, Field(ge=0)] | None = None
    temporary_percent: Annotated[float, Field(ge=0)] | None = None
    temporary_start: datetime | None = None
    temporary_end: datetime | None = None
    old_percent: Annotated[float, Field(ge=0)] | None = None
    auto_pay: Annotated[int, Field(ge=0)] | None = None
    auto_pay_limit: Annotated[float, Field(ge=0)] | None = None
    past_auto_pay_limit: Annotated[float, Field(ge=0)] | None = None
    last_auto_pay: datetime | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class PartnerCreate(PartnerBase):
    password: Annotated[str, MinLen(6), MaxLen(200)]
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr]


class PartnerUpdate(PartnerBase):
    password: Annotated[str, MinLen(6), MaxLen(200)] | None = None


class Partner(PartnerBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PartnerMin(BaseModel):
    id: int
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr]
