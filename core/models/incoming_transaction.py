import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Enum, text, Date, DateTime, ForeignKey, JSON
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func

import enum


class StatusChoices(enum.Enum):
    Completed = 'Completed'
    Authorized = 'Authorized'
    Declined = 'Declined'


class NStatusChoices(enum.Enum):
    NO = 'NO'
    GOOD = 'GOOD'
    BAD = 'BAD'


class TypeChoices(enum.Enum):
    Payment = 'Payment'
    Refund = 'Refund'
    CardPayout = 'CardPayout'


class PaymentTypeChoices(enum.Enum):
    SUBSCRIPTION = 'SUBSCRIPTION'
    REBILL = 'REBILL'
    NO = 'NO'
    NOT_DETECTED = 'NOT_DETECTED'


class CurrencyChoices(enum.Enum):
    RUR = 'RUR'
    USD = 'USD'
    EUR = 'EUR'


class IncomingTransaction(Base):
    payment_system: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    amount: Mapped[float] = mapped_column(
        nullable=False
    )

    currency: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    payment_amount: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    payment_currency: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    create_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    create_date_day: Mapped[date | None] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
        nullable=True,
    )

    create_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
        nullable=True,
    )

    card_first_six: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    card_last_four: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    card_type: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    card_exp_date: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True
    )

    test_mode: Mapped[int] = mapped_column(
        nullable=False,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(10),
        Enum(StatusChoices),
        nullable=False
    )

    operation_type: Mapped[str] = mapped_column(
        String(10),
        Enum(TypeChoices),
        nullable=False
    )

    gateway_name: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    invoice_id: Mapped[int | None] = mapped_column(
        ForeignKey("invoices.id", ondelete="SET NULL"),
        nullable=True
    )

    account_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    subscription_id: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    email: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    ip_country: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True
    )

    ip_city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    ip_region: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    ip_district: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    ip_latitude: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    ip_longitude: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    issuer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    issuer_bank_country: Mapped[str | None] = mapped_column(
        String(3),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    auth_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    data: Mapped[str | None] = mapped_column(
        JSON,
        nullable=True
    )

    token: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    total_fee: Mapped[float | None] = mapped_column(
        nullable=True
    )

    card_product: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    payment_method: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    fall_back_scenario_declined_transaction_id: Mapped[int | None] = mapped_column(
        nullable=True
    )

    error: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    custom_error: Mapped[int | None] = mapped_column(
        ForeignKey("transactionerrors.id", ondelete="SET NULL"),
        nullable=True
    )

    n_invoice_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_subscription_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_client_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_host_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_partner_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_stream_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_offer_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_landing_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_manager_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    n_terminal_id: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(12),
        Enum(PaymentTypeChoices),
        default=PaymentTypeChoices.NO.value,
        server_default=PaymentTypeChoices.NO.value,
        nullable=False
    )

    n_status: Mapped[str] = mapped_column(
        String(4),
        Enum(NStatusChoices),
        default=NStatusChoices.NO.value,
        server_default=NStatusChoices.NO.value,
        nullable=False
    )

    technical: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    charge_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    charge_date_pay: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    refund: Mapped[int] = mapped_column(
        default=0,
        server_default=text("0"),
        nullable=False
    )

    added_currency: Mapped[str] = mapped_column(
        String(10),
        Enum(CurrencyChoices),
        default=CurrencyChoices.RUR.value,
        server_default=CurrencyChoices.RUR.value,
        nullable=False
    )

    error_desc_ru: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    error_desc_en: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )
