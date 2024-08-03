from datetime import datetime, date

from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, Field

from core.models.payout_requisite import StatusChoices


class BasePayoutRequisite(BaseModel):
    type: Annotated[str, MaxLen(250)] | None = None
    status: Annotated[str, Optional["StatusChoices"]] | None = None
    partner_id: Annotated[int, Field(gt=0)] | None = None
    manager_id: Annotated[int, Field(gt=0)] | None = None

    data: str | None = None
    name_data: Annotated[str, MaxLen(100)] | None = None
    surname_data: Annotated[str, MaxLen(100)] | None = None

    capitalist: Annotated[str, MaxLen(100)] | None = None

    webmoney: Annotated[str, MaxLen(100)] | None = None

    qiwi: Annotated[str, MaxLen(100)] | None = None

    umoney: Annotated[str, MaxLen(100)] | None = None

    data_card_to_card: Annotated[str, MaxLen(100)] | None = None

    data_mastercard_worldwide: Annotated[str, MaxLen(100)] | None = None
    month_mc: Annotated[str, MaxLen(2)] | None = None
    year_mc: Annotated[str, MaxLen(4), MinLen(4)] | None = None
    name_mc: Annotated[str, MaxLen(100)] | None = None
    surname_mc: Annotated[str, MaxLen(100)] | None = None
    birth_date_mc: Annotated[str, MaxLen(20)] | None = None
    country_code_mc: Annotated[str, MaxLen(3)] | None = None
    city_mc: Annotated[str, MaxLen(100)] | None = None
    address_mc: Annotated[str, MaxLen(250)] | None = None

    usdt_erc_20: Annotated[str, MaxLen(200)] | None = None

    usdt_trc_20: Annotated[str, MaxLen(200)] | None = None

    ip_name: Annotated[str, MaxLen(250)] | None = None
    ip_address: Annotated[str, MaxLen(250)] | None = None
    ip_inn: Annotated[str, MaxLen(25)] | None = None
    ip_ogrn: Annotated[str, MaxLen(250)] | None = None
    ip_rs: Annotated[str, MaxLen(250)] | None = None
    ip_bank: Annotated[str, MaxLen(250)] | None = None
    ip_bank_inn: Annotated[str, MaxLen(250)] | None = None
    ip_bank_bik: Annotated[str, MaxLen(250)] | None = None
    ip_bank_ks: Annotated[str, MaxLen(250)] | None = None

    oooru_name: Annotated[str, MaxLen(250)] | None = None
    oooru_address: Annotated[str, MaxLen(250)] | None = None
    oooru_inn: Annotated[str, MaxLen(250)] | None = None
    oooru_kpp: Annotated[str, MaxLen(250)] | None = None
    oooru_ogrn: Annotated[str, MaxLen(250)] | None = None
    oooru_rs: Annotated[str, MaxLen(250)] | None = None
    oooru_bank: Annotated[str, MaxLen(250)] | None = None
    oooru_bank_inn: Annotated[str, MaxLen(250)] | None = None
    oooru_bank_bik: Annotated[str, MaxLen(250)] | None = None
    oooru_bank_ks: Annotated[str, MaxLen(250)] | None = None

    data_kz: str | None = None
    name_data_kz: Annotated[str, MaxLen(100)] | None = None
    surname_data_kz: Annotated[str, MaxLen(100)] | None = None

    self_employed_tinkoff: str | None = None
    self_employed_tinkoff_fio: str | None = None

    self_employed: str | None = None
    self_employed_fio: str | None = None
    self_employed_phone: str | None = None
    self_employed_inn: str | None = None
    self_employed_bik: str | None = None


class PaySystemUpdate(BasePayoutRequisite):
    pass


class PayoutRequisite(BasePayoutRequisite):
    model_config = ConfigDict(from_attributes=True)

    id: int

    add_date: datetime
    add_date_day: date
    add_date_hour: int

    change_date: datetime
    change_date_day: date
    change_date_hour: int
