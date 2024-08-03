from typing import Optional, Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field, UUID4
from datetime import datetime, date

from core.models.host import DeviceChoices


class HostBase(BaseModel):
    uuid: UUID4
    partner_id: Annotated[int, Field(gt=0)] | None = None
    manager_id: Annotated[int, Field(gt=0)] | None = None
    stream_id: Annotated[int, Field(gt=0)] | None = None
    landing_id: Annotated[int, Field(gt=0)] | None = None
    n_partner_id: Annotated[int, Field(ge=0)] | None = None
    n_manager_id: Annotated[int, Field(ge=0)] | None = None
    n_stream_id: Annotated[int, Field(ge=0)] | None = None
    n_landing_id: Annotated[int, Field(ge=0)] | None = None
    n_offer_id: Annotated[int, Field(ge=0)] | None = None
    version: Annotated[int, Field(ge=0)] | None = None
    create_date: datetime | None = None
    create_date_day: date | None = None
    create_date_hour: Annotated[int, Field(ge=0)] | None = None
    country_id: Annotated[str, MaxLen(500)] | None = None
    os_id: Annotated[str, MaxLen(500)] | None = None
    device_type: Annotated[str, Optional[DeviceChoices]] | None = None
    browser_id: Annotated[str, MaxLen(100)] | None = None
    ref_domain_id: Annotated[str, MaxLen(2000)] | None = None
    referrer_id: Annotated[str, MaxLen(2000)] | None = None
    ipv4: Annotated[str, MaxLen(100)] | None = None
    utm_source: Annotated[str, MaxLen(500)] | None = None
    utm_medium: Annotated[str, MaxLen(500)] | None = None
    utm_campaign: Annotated[str, MaxLen(500)] | None = None
    utm_content: Annotated[str, MaxLen(500)] | None = None
    utm_term: Annotated[str, MaxLen(500)] | None = None
    sub_1: Annotated[str, MaxLen(255)] | None = None
    sub_2: Annotated[str, MaxLen(255)] | None = None
    sub_3: Annotated[str, MaxLen(255)] | None = None
    sub_4: Annotated[str, MaxLen(255)] | None = None
    sub_5: Annotated[str, MaxLen(255)] | None = None
    click_id: Annotated[str, MaxLen(500)] | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class HostCreate(HostBase):
    pass


class HostUpdate(HostBase):
    uuid: UUID4 | None = None


class Host(HostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
