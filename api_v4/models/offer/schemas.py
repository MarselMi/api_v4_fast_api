from datetime import datetime, date

from pydantic import BaseModel, Field, ConfigDict
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen
from core.models.offer import StatusChoices, TypeChoices, CurrencyChoices

from api_v4.models.partner.schemas import PartnerMin


class OfferBase(BaseModel):
    name: Annotated[str, MaxLen(255)] | None = None
    logo: Annotated[str, MaxLen(500)] | None = None
    geo: Annotated[str, MaxLen(255)] | None = None
    deduction: Annotated[float, Field(ge=0)] | None = None
    rebill: Annotated[float, Field(ge=0)] | None = None
    trial: Annotated[int, Field(ge=0)] | None = None
    payments_periodicity: Annotated[int, Field(ge=0)] | None = None
    unexepted_traffic: str | None = None
    main_domain: Annotated[str, MaxLen(500)] | None = None
    description: Annotated[str, MaxLen(1000)] | None = None
    screenshot: str | None = None
    status: Annotated[str, Optional["StatusChoices"]] | None = None
    type: Annotated[str, Optional["TypeChoices"]] | None = None
    author_pay: Annotated[int, Field(ge=0)] | None = None
    subs_pay: Annotated[int, Field(ge=0)] | None = None
    author_percent: Annotated[float, Field(ge=0)] | None = None
    first_pay: Annotated[float, Field(ge=0)] | None = None
    create_date: datetime | None = None
    create_date_day: date | None = None
    create_date_hour: Annotated[int, Field(gt=0)] | None = None
    change_date: datetime | None = None
    change_date_day: date | None = None
    change_date_hour: Annotated[int, Field(gt=0)] | None = None
    cash_register_number: Annotated[str, MaxLen(250)] | None = None
    inn: Annotated[str, MinLen(10), MaxLen(12)] | None = None
    rebill_low: Annotated[float, Field(ge=0)] | None = None
    rebill_low_period: Annotated[float, Field(ge=0)] | None = None
    conf_data: str | None = None
    user_stats_reports: Annotated[str, MaxLen(128)] | None = None
    payment_place: Annotated[str, MaxLen(250)] | None = None
    payment_description: str | None = None
    currency: Annotated[str, Optional["CurrencyChoices"], MaxLen(4)] | None = None
    private_partners: list["PartnerMin"] | None = None
    default_terminal_id: int | None = None
    manager_id: Annotated[int, Field(gt=0)] | None = None
    # manager: Optional["ManagerMin"] = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class OfferCreate(OfferBase):
    name: Annotated[str, MinLen(1), MaxLen(255)]
    rebill: Annotated[float, Field(ge=0)]
    trial: Annotated[int, Field(ge=0)]
    payments_periodicity: Annotated[int, Field(ge=0)]
    private_partners: list[Annotated[int, Field(gt=0)]] | None = None
    main_domain: Annotated[str, MinLen(5), MaxLen(500)]


class OfferUpdate(OfferBase):
    private_partners: list[Annotated[int, Field(gt=0)]] | None = None
    # manager: int | None = None


class Offer(OfferBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class OfferRel(Offer):
    private_partners: list["PartnerMin"] | None
    # manager: Optional["ManagerMin"]


class OfferMin(BaseModel):
    id: int
    name: str
