from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class PaySystemBase(BaseModel):
    code: Annotated[str, MaxLen(250)] | None = None
    title: Annotated[str, MaxLen(500)] | None = None


class PaySystemCreate(PaySystemBase):
    code: Annotated[str, MaxLen(250)]
    title: Annotated[str, MaxLen(500)]


class PaySystemUpdate(PaySystemBase):
    pass


class PaySystem(PaySystemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
