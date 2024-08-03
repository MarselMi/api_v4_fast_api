from pydantic import BaseModel, ConfigDict
from typing import Annotated
from annotated_types import MinLen, MaxLen


class OrganisationBase(BaseModel):
    title: Annotated[str, MaxLen(500)] | None = None
    inn: Annotated[str, MinLen(10), MaxLen(12)] | None = None


class OrganisationCreate(OrganisationBase):
    title: Annotated[str, MaxLen(500)]
    inn: Annotated[str, MinLen(10), MaxLen(12)]


class OrganisationUpdate(OrganisationBase):
    pass


class Organisation(OrganisationBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
