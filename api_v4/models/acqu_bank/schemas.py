from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class AcquBankBase(BaseModel):
    code: str | None = None
    name: Annotated[str, MaxLen(60)] | None = None
    title: Annotated[str, MaxLen(500)] | None = None


class AcquBankCreate(AcquBankBase):
    code: str
    name: Annotated[str, MaxLen(60)]
    title: Annotated[str, MaxLen(500)]


class AcquBankUpdate(AcquBankBase):
    pass


class AcquBank(AcquBankBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
