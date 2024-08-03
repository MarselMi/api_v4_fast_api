from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class EventBase(BaseModel):
    name: Annotated[str, MaxLen(64)] | None = None


class EventCreate(EventBase):
    name: Annotated[str, MaxLen(64)]


class EventUpdate(EventBase):
    pass


class Event(EventBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
