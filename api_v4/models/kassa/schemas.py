from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated
from annotated_types import MaxLen


class KassaBase(BaseModel):
    number: Annotated[str, MaxLen(100)] | None = None
    status: Annotated[int, Field(gt=0)] | None = None
    used_in_pay: Annotated[int, Field(ge=0)] | None = None
    login: Annotated[str, MaxLen(250)] | None = None
    password: Annotated[str, MaxLen(250)] | None = None
    organisation_id: Annotated[int, Field(gt=0)] | None = None
    kass_type: str | None = None


class KassaCreate(KassaBase):
    login: Annotated[str, MaxLen(250)]
    password: Annotated[str, MaxLen(250)]
    organisation_id: Annotated[int, Field(gt=0)]
    kass_type: str


class KassaUpdate(KassaBase):
    pass


class Kassa(KassaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class KassaRel(Kassa):
    # organisation: Optional["Organisation"] | None = None
    pass
