from typing import Annotated

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime, date


class CreatePartnerAction(BaseModel):
    act_type: Annotated[str, MaxLen(250)]
    manager: Annotated[int, Field(gt=0)]
    partner: Annotated[int, Field(gt=0)]
    ip: Annotated[str, MaxLen(100)]
    action: str


class PartnerAction(CreatePartnerAction):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_date: datetime
    create_date_day: date
