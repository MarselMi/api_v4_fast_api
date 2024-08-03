from pydantic import BaseModel
from core.models.kass_type import MethodChoices
from typing import Annotated, Optional
from annotated_types import MinLen, MaxLen


class KassTypeBase(BaseModel):
    title: Annotated[str, MaxLen(500)] | None = None
    method: Annotated[str, Optional[MethodChoices]] | None = None
    link: str | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class KassTypeCreate(KassTypeBase):
    title: Annotated[str, MaxLen(500)]
    link: str


class KassTypeUpdate(KassTypeBase):
    pass


class KassType(KassTypeBase):
    id: int
