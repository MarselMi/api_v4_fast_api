from typing import Annotated, Optional

from datetime import datetime, date

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr, Field, UUID4

from uuid import uuid4

from core.models.client import StatusChoices


class ClientBase(BaseModel):
    uuid: UUID4 | None = None
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr] | None = None
    phone: Annotated[str, MaxLen(20)] | None = None

    create_date: datetime | None = None
    create_date_day: date | None = None
    create_date_hour: Annotated[int, Field(ge=0)] | None = None

    change_date: datetime | None = None
    change_date_day: date | None = None
    change_date_hour: Annotated[int, Field(ge=0)] | None = None

    offer_id: Annotated[int, Field(gt=0)] | None = None
    host_id: Annotated[int, Field(gt=0)] | None = None
    status: Annotated[str, Optional["StatusChoices"]] | None = None

    last_auth_date: datetime | None = None
    last_auth_date_day: date | None = None
    last_auth_date_hour: Annotated[int, Field(ge=0)] | None = None

    first_subscribe_date: datetime | None = None
    first_subscribe_day: date | None = None
    first_subscribe_hour: Annotated[int, Field(ge=0)] | None = None

    is_subscribed: Annotated[int, Field(ge=0)] | None = None
    data: str | None = None

    n_host_id: Annotated[int, Field(ge=0)] | None = None
    n_partner_id: Annotated[int, Field(ge=0)] | None = None
    n_stream_id: Annotated[int, Field(ge=0)] | None = None
    n_landing_id: Annotated[int, Field(ge=0)] | None = None
    n_offer_id: Annotated[int, Field(ge=0)] | None = None
    n_manager_id: Annotated[int, Field(ge=0)] | None = None

    active: Annotated[int, Field(ge=0)] | None = None
    card_first_six: Annotated[str, MaxLen(10), MinLen(6)] | None = None
    card_last_four: Annotated[str, MaxLen(10), MinLen(4)] | None = None
    technical: Annotated[int, Field(ge=0)] | None = None
    tech_show: Annotated[int, Field(ge=0)] | None = None
    note: str | None = None
    last_call: datetime | None = None
    charge_date: datetime | None = None
    tech_reb_count: Annotated[int, Field(ge=0)] | None = None
    contacts: str | None = None
    pre_payment_request: datetime | None = None


class ClientCreate(ClientBase):
    password: Annotated[str, MinLen(6)]
    offer_id: Annotated[int, Field(gt=0)]
    card_first_six: Annotated[str, MaxLen(10), MinLen(6)]
    card_last_four: Annotated[str, MaxLen(10), MinLen(4)]


class Client(ClientBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class ClientUpdate(ClientBase):
    password: Annotated[str, MinLen(6)] | None = None


class ClientAuth(BaseModel):
    password: Annotated[str, MinLen(6)] | None = None
    offer_id: Annotated[int, Field(gt=0)] | None = None
    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr] | None = None
    phone: Annotated[str, MaxLen(20)] | None = None
