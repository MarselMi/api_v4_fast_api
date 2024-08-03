from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, Field, EmailStr
from datetime import datetime, date


class CreateOperatorAction(BaseModel):
    manager_id: Annotated[int, Field(gt=0)] | None = None
    client_id: Annotated[int, Field(gt=0)]

    email: Annotated[str, MinLen(5), MaxLen(25), EmailStr] | None = None
    phone: Annotated[str, MaxLen(100)] | None = None

    card: Annotated[str, MaxLen(50)]
    action: Annotated[str, MaxLen(250)]
    description: str


class OperatorAction(CreateOperatorAction):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_date: datetime
    create_date_day: date
