from pydantic import BaseModel, ConfigDict, Field
from typing import Annotated, Optional
from datetime import datetime, date
from core.models.postback import StatusChoices, MethodChoices

from api_v4.models.event.schemas import Event


class PostbackBase(BaseModel):

    partner_id: Annotated[int, Field(gt=0)] | None = None
    manager_id: Annotated[int, Field(gt=0)] | None = None
    name: str | None = None
    method: Annotated[str, Optional[MethodChoices]] | None = None
    event_id: list["Event"] | None = None
    link: str | None = None
    postdata: str | None = None
    status: Annotated[str, Optional[StatusChoices]] | None = None

    created: datetime | None = None
    created_day: date | None = None
    created_hour: Annotated[int, Field(ge=0)] | None = None

    change_date: datetime | None = None
    change_date_day: date | None = None
    change_date_hour: Annotated[int, Field(ge=0)] | None = None


class PostbackCreate(PostbackBase):
    name: str
    link: str
    partner_id: Annotated[int, Field(gt=0)]
    method: Annotated[str, Optional[MethodChoices]]
    event_id: list[Annotated[int, Field(gt=0)]] | None = None


class PostbackUpdate(PostbackBase):
    event_id: list[Annotated[int, Field(gt=0)]]


class Postback(PostbackBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PostbackMin(BaseModel):
    id: int
    name: str
