from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field

from core.models.transaction_error import ActionChoices


class TrErrorBase(BaseModel):
    paysystem: Annotated[str, MaxLen(100)] | None = None
    code: Annotated[int, Field(ge=0)] | None = None
    string_code: Annotated[str, MaxLen(500)] | None = None
    name: Annotated[str, MaxLen(500)] | None = None
    action: Annotated[str, Optional["ActionChoices"]] | None = None

    create_date: datetime | None = None
    change_date: datetime | None = None
    created_hour: Annotated[int, Field(ge=0)] | None = None


class TrErrorCreate(TrErrorBase):
    code: Annotated[str, MaxLen(250)]
    title: Annotated[str, MaxLen(500)]
    name: Annotated[str, MaxLen(500)]


class TrErrorUpdate(TrErrorBase):
    pass


class TrError(TrErrorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
