from typing import Annotated, Optional
from datetime import datetime, date

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict, Field

from core.models.subscription import UnsubChoices, TypeChoices, StatusChoices


class SubscriptionBase(BaseModel):
    client_id: Annotated[int, Field(gt=0)] | None = None
    type: Annotated[str, Optional["TypeChoices"]] | None = None
    now_type: Annotated[int, Field(ge=0)] | None = None

    create_date: datetime | None = None
    create_date_day: date | None = None
    create_date_hour: Annotated[int, Field(ge=0)] | None = None

    unsub_date: datetime | None = None
    unsub_date_day: date | None = None
    unsub_date_hour: Annotated[int, Field(ge=0)] | None = None

    start_date: datetime | None = None
    start_date_day: date | None = None
    start_date_hour: Annotated[int, Field(ge=0)] | None = None

    try_date: datetime | None = None
    try_date_day: date | None = None
    try_date_hour: Annotated[int, Field(ge=0)] | None = None

    two_try_date: datetime | None = None
    two_try_date_day: date | None = None
    two_try_date_hour: Annotated[int, Field(ge=0)] | None = None

    pay_date: datetime | None = None
    pay_date_day: date | None = None
    pay_date_hour: Annotated[int, Field(ge=0)] | None = None

    two_pay_date: datetime | None = None
    two_pay_date_day: date | None = None
    two_pay_date_hour: Annotated[int, Field(ge=0)] | None = None

    is_unsub: Annotated[int, Field(ge=0)] | None = None
    tarif_name: Annotated[str, MaxLen(250)] | None = None
    two_tarif_name: Annotated[str, MaxLen(250)] | None = None
    tarif_sum: Annotated[float, Field(ge=0)] | None = None
    two_tarif_sum: Annotated[float, Field(ge=0)] | None = None
    status: Annotated[str, Optional["StatusChoices"]] | None = None
    is_start: Annotated[int, Field(ge=0)] | None = None

    try_count: Annotated[int, Field(ge=0)] | None = None
    two_try_count: Annotated[int, Field(ge=0)] | None = None
    count_fail: Annotated[int, Field(ge=0)] | None = None

    period: Annotated[int, Field(ge=0)] | None = None
    two_period: Annotated[int, Field(ge=0)] | None = None
    freeday: Annotated[int, Field(ge=0)] | None = None
    two_freeday: Annotated[int, Field(ge=0)] | None = None

    transaction_id: Annotated[int, Field(gt=0)] | None = None

    card_number: Annotated[str, MaxLen(50)] | None = None
    token: Annotated[str, MaxLen(255)] | None = None
    count_good: Annotated[int, Field(ge=0)] | None = None
    time_good: Annotated[float, Field(ge=0)] | None = None

    n_client_id: Annotated[int, Field(ge=0)] | None = None
    n_host_id: Annotated[int, Field(ge=0)] | None = None
    n_partner_id: Annotated[int, Field(ge=0)] | None = None
    n_stream_id: Annotated[int, Field(ge=0)] | None = None
    n_landing_id: Annotated[int, Field(ge=0)] | None = None
    n_offer_id: Annotated[int, Field(ge=0)] | None = None
    n_manager_id: Annotated[int, Field(ge=0)] | None = None
    n_terminal_id: Annotated[int, Field(ge=0)] | None = None

    profit: Annotated[float, Field(ge=0)] | None = None
    type_unsub: Annotated[str, Optional["UnsubChoices"]] | None = None
    type_unsub_id: Annotated[int, Field(ge=0)] | None = None
    type_unsub_val: Annotated[int, Field(ge=0)] | None = None
    terminal_id: Annotated[int, Field(gt=0)] | None = None
    added_rebill_period: Annotated[int, Field(ge=0)] | None = None
    error: Annotated[int, Field(gt=0)] | None = None
    try_interval_days: Annotated[int, Field(ge=0)] | None = None
    try_interval_days_def: Annotated[int, Field(ge=0)] | None = None
    is_tariff_updated: Annotated[int, Field(ge=0)] | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class SubscriptionCreate(SubscriptionBase):
    period: Annotated[int, Field(ge=0)]
    tarif_name: Annotated[str, MaxLen(250)]
    tarif_sum: Annotated[float, Field(ge=0)]


class SubscriptionUpdate(SubscriptionBase):
    pass


class Subscription(SubscriptionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
