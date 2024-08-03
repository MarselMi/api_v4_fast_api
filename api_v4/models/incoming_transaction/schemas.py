from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date


class CloudPaymentsTransaction(BaseModel):
    TransactionId: int
    amount: float
    currency: str
    payment_amount: float
    payment_currency: str
    operation_type: str
    invoice_id: int
    account_id: str
    subscription_id: str = ''
    name: str = ''
    email: str = ''
    create_date: str
    ip_address: str
    ip_country: str
    ip_city: str
    ip_region: str
    ip_district: str
    ip_latitude: str
    ip_longitude: str
    cardid: str = ''
    card_first_six: str
    card_last_four: str
    card_type: str
    card_exp_date: str
    issuer: str
    issuer_bank_country: str
    description: str = ''
    test_mode: bool
    status: str
    statuscode: str
    reason: str
    ReasonCode: str
    payment_method: str = ''
    token: str
    rrn: str

    class Config:
        allow_extra = True


class PaySelectionTransaction(BaseModel):
    Event: str
    Amount: float
    Currency: str
    DateTime: str
    IsTest: bool
    Brand: str
    Bank: str = ''
    CountryCodeAlpha2: str
    TransactionId: str
    OrderId: str
    Description: str = ''
    CustomFields: str = ''
    Service_Id: str
    PaymentMethod: str
    CardMasked: str
    ErrorMessage: str = ''
    ExpirationDate: str
    RRN: str
    CardHolder: str
    ErrorCode: str = ''
    ClientMessage: str = ''
    NewAmount: Optional[float] = None
    Country_Code_Alpha2: Optional[str] = None
    RebillId: Optional[str] = None

    class Config:
        allow_extra = True


class StatusChoices(str, Enum):
    Completed = 'Completed'
    Authorized = 'Authorized'
    Declined = 'Declined'


class NStatusChoices(str, Enum):
    NO = 'NO'
    GOOD = 'GOOD'
    BAD = 'BAD'


class TypeChoices(str, Enum):
    Payment = 'Payment'
    Refund = 'Refund'
    CardPayout = 'CardPayout'


class PaymentTypeChoices(str, Enum):
    SUBSCRIPTION = 'SUBSCRIPTION'
    REBILL = 'REBILL'
    NO = 'NO'
    NOT_DETECTED = 'NOT_DETECTED'


class CurrencyChoices(str, Enum):
    RUR = 'RUR'
    USD = 'USD'
    EUR = 'EUR'


class IncomingTransactionBase(BaseModel):
    payment_system: Optional[str]
    amount: float
    currency: str
    payment_amount: Optional[str]
    payment_currency: Optional[str]
    create_date: Optional[datetime]
    create_date_day: Optional[date]
    create_date_hour: Optional[str]
    card_first_six: Optional[str]
    card_last_four: Optional[str]
    card_type: Optional[str]
    card_exp_date: Optional[str]
    test_mode: int = 0
    status: StatusChoices
    operation_type: TypeChoices
    gateway_name: Optional[str]
    invoice_id: Optional[int]
    account_id: Optional[str]
    subscription_id: Optional[str]
    name: Optional[str]
    email: Optional[str]
    ip_address: Optional[str]
    ip_country: Optional[str]
    ip_city: Optional[str]
    ip_region: Optional[str]
    ip_district: Optional[str]
    ip_latitude: Optional[str]
    ip_longitude: Optional[str]
    issuer: Optional[str]
    issuer_bank_country: Optional[str]
    description: Optional[str]
    auth_code: Optional[str]
    data: Optional[str]
    token: Optional[str]
    total_fee: Optional[float]
    card_product: Optional[str]
    payment_method: Optional[str]
    fall_back_scenario_declined_transaction_id: Optional[int]
    error: Optional[str]
    custom_error: Optional[int]
    n_invoice_id: int = 0
    n_subscription_id: int = 0
    n_client_id: int = 0
    n_host_id: int = 0
    n_partner_id: int = 0
    n_stream_id: int = 0
    n_offer_id: int = 0
    n_landing_id: int = 0
    n_manager_id: int = 0
    n_terminal_id: int = 0
    type: PaymentTypeChoices = PaymentTypeChoices.NO
    n_status: NStatusChoices = NStatusChoices.NO
    technical: int = 0
    charge_date: Optional[datetime]
    charge_date_pay: Optional[datetime]
    refund: int = 0
    added_currency: CurrencyChoices = CurrencyChoices.RUR
    error_desc_ru: Optional[str]
    error_desc_en: Optional[str]

    class Config:
        orm_mode = True


class IncomingTransactionCreate(IncomingTransactionBase):
    pass


class IncomingTransactionUpdate(IncomingTransactionBase):
    pass


class IncomingTransaction(IncomingTransactionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
