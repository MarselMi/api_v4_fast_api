from typing import Annotated
from datetime import datetime, date

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field

from api_v4.models.postback.schemas import PostbackMin


class StreamBase(BaseModel):
    name: Annotated[str, MaxLen(64)] | None = None
    partner_id: Annotated[int, Field(gt=0)] | None = None
    manager_id: Annotated[int, Field(gt=0)] | None = None
    offer_id: Annotated[int, Field(gt=0)] | None = None
    landing_id: Annotated[int, Field(gt=0)] | None = None
    prelanding_id: Annotated[int, Field(gt=0)] | None = None
    uid: int | None = None
    postback_id: list["PostbackMin"] | None = None
    link: str | None = None
    yandex_id: str | None = None
    yandex_metric: str | None = None
    google_analytics: str | None = None
    top_mail_ru: str | None = None
    facebook_pixel: str | None = None
    vk_counter: str | None = None
    tiktok_pixel: str | None = None
    landingelement_data: str | None = None

    created_date: datetime | None = None
    created_day: date | None = None
    created_hour: Annotated[int, Field(ge=0)] | None = None

    change_date: datetime | None = None
    change_date_day: date | None = None
    change_date_hour: Annotated[int, Field(ge=0)] | None = None


class StreamCreate(StreamBase):
    name: Annotated[str, MaxLen(64)]
    offer_id: Annotated[int, Field(gt=0)]
    landing_id: Annotated[int, Field(gt=0)]
    partner_id: Annotated[int, Field(gt=0)]
    postback_id: list[Annotated[int, Field(gt=0)]] | None = None


class StreamUpdate(StreamBase):
    postback_id: list[Annotated[int, Field(gt=0)]] | None = None


class Stream(StreamBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
