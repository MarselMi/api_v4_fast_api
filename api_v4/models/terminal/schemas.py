from datetime import datetime
from typing import Annotated, Optional

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field

from core.models.terminal import CurrencyChoices


class TerminalBase(BaseModel):
    offer_id: Annotated[int, Field(gt=0)] | None = None
    paysystem_id: Annotated[int, Field(gt=0)] | None = None
    organisation_id: Annotated[int, Field(gt=0)] | None = None
    kassa_id: Annotated[int, Field(gt=0)] | None = None
    acqu_bank: Annotated[int, Field(gt=0)] | None = None

    title: Annotated[str, MaxLen(500)] | None = None
    paysystem_public_id: Annotated[str, MaxLen(500)] | None = None
    paysystem_secret_key: Annotated[str, MaxLen(500)] | None = None
    paysystem_service_id: Annotated[str, MaxLen(500)] | None = None
    currency: Annotated[str, Optional["CurrencyChoices"]] | None = None
    paysystem_service_name: str | None = None
    status: str | None = None

    one_time_pay: Annotated[int, Field(ge=0)] | None = None
    contains_rebills: Annotated[int, Field(ge=0)] | None = None
    rebills: Annotated[int, Field(ge=0)] | None = None
    percent: Annotated[int, Field(ge=0)] | None = None
    selected: Annotated[int, Field(ge=0)] | None = None
    rebill_terminal_id: Annotated[int, Field(ge=0)] | None = None


class TerminalCreate(TerminalBase):
    title: Annotated[str, MaxLen(500)]
    paysystem_service_id: Annotated[str, MaxLen(500)]
    paysystem_public_id: Annotated[str, MaxLen(500)]
    paysystem_secret_key: Annotated[str, MaxLen(500)]


class TerminalUpdate(TerminalBase):
    pass


class Terminal(TerminalBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
