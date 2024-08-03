import pytz
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Enum, Text, text, Date, DateTime, ForeignKey
from core.models import Base
from datetime import datetime, date
from sqlalchemy.sql import func
from core.payment_basics import PAYMENT_BASICS

import enum


class StatusChoices(enum.Enum):
    ACTIVE = "Активные"
    BLOCK = "Заблокированы"
    DELETE = "Удалены"


class PayoutRequisite(Base):
    type: Mapped[str] = mapped_column(String(250), nullable=False)

    partner_id: Mapped[int | None] = mapped_column(
        ForeignKey("partners.id", ondelete="SET NULL"), nullable=True
    )

    # partners: Mapped["Partner"] = relationship(
    #     back_populates="partners"
    # )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("managers.id", ondelete="SET NULL"), nullable=True
    )

    # managers: Mapped["Manager"] = relationship(
    #     back_populates="managers"
    # )

    add_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")),
    )

    add_date_day: Mapped[date] = mapped_column(
        Date,
        server_default=text("(CURRENT_DATE)"),
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )

    add_date_hour: Mapped[str] = mapped_column(
        String(2),
        server_default=f"{datetime.now().hour}",
        default=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )

    change_date: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=None,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")),
        nullable=True,
    )

    change_date_day: Mapped[date | None] = mapped_column(
        Date,
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).date,
    )

    change_date_hour: Mapped[str | None] = mapped_column(
        String(2),
        default=None,
        nullable=True,
        onupdate=datetime.now(tz=pytz.timezone("Europe/Moscow")).hour,
    )

    data: Mapped[str | None] = mapped_column(Text, nullable=True)

    name_data: Mapped[str | None] = mapped_column(String(100), nullable=True)

    surname_data: Mapped[str | None] = mapped_column(String(100), nullable=True)

    data_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_PARTNER_PERCENT')}"),
        nullable=False,
    )
    data_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_PARTNER_FIX')}"),
        nullable=False,
    )
    data_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_SYSTEM_PERCENT')}"),
        nullable=False,
    )
    data_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_SYSTEM_FIX')}"),
        nullable=False,
    )

    status: Mapped[str | None] = mapped_column(
        String(50),
        Enum(StatusChoices),
        server_default=StatusChoices.ACTIVE.value,
        default=StatusChoices.ACTIVE.value,
    )

    capitalist: Mapped[str | None] = mapped_column(String(100), nullable=True)

    capitalist_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("CAPITALIST_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('CAPITALIST_PARTNER_PERCENT')}"),
        nullable=False,
    )

    capitalist_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("CAPITALIST_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('CAPITALIST_PARTNER_FIX')}"),
        nullable=False,
    )

    capitalist_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("CAPITALIST_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('CAPITALIST_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    capitalist_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("CAPITALIST_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('CAPITALIST_SYSTEM_FIX')}"),
        nullable=False,
    )

    webmoney: Mapped[str | None] = mapped_column(String(100), nullable=True)

    webmoney_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("WEB_MONEY_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('WEB_MONEY_PARTNER_PERCENT')}"),
        nullable=False,
    )

    webmoney_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("WEB_MONEY_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('WEB_MONEY_PARTNER_FIX')}"),
        nullable=False,
    )

    webmoney_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("WEB_MONEY_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('WEB_MONEY_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    webmoney_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("WEB_MONEY_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('WEB_MONEY_SYSTEM_FIX')}"),
        nullable=False,
    )

    qiwi: Mapped[str | None] = mapped_column(String(100), nullable=True)

    qiwi_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("QIWI_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('QIWI_PARTNER_PERCENT')}"),
        nullable=False,
    )

    qiwi_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("QIWI_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('QIWI_PARTNER_FIX')}"),
        nullable=False,
    )

    qiwi_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("QIWI_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('QIWI_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    qiwi_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("QIWI_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('QIWI_SYSTEM_FIX')}"),
        nullable=False,
    )

    umoney: Mapped[str | None] = mapped_column(String(100), nullable=True)

    umoney_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("U_MONEY_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('U_MONEY_PARTNER_PERCENT')}"),
        nullable=False,
    )

    umoney_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("U_MONEY_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('U_MONEY_PARTNER_FIX')}"),
        nullable=False,
    )

    umoney_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("U_MONEY_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('U_MONEY_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    umoney_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("U_MONEY_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('U_MONEY_SYSTEM_FIX')}"),
        nullable=False,
    )

    data_card_to_card: Mapped[str | None] = mapped_column(String(100), nullable=True)

    data_card_to_card_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_CARD_TO_CARD_PARTNER_PERCENT"),
        server_default=text(
            f"{PAYMENT_BASICS.get('DATA_CARD_TO_CARD_PARTNER_PERCENT')}"
        ),
        nullable=False,
    )

    data_card_to_card_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_CARD_TO_CARD_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_CARD_TO_CARD_PARTNER_FIX')}"),
        nullable=False,
    )

    data_card_to_card_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_CARD_TO_CARD_SYSTEM_PERCENT"),
        server_default=text(
            f"{PAYMENT_BASICS.get('DATA_CARD_TO_CARD_SYSTEM_PERCENT')}"
        ),
        nullable=False,
    )

    data_card_to_card_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_CARD_TO_CARD_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_CARD_TO_CARD_SYSTEM_FIX')}"),
        nullable=False,
    )

    data_mastercard_worldwide: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )

    data_mastercard_worldwide_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_MASTERCARD_WORLDWIDE_PARTNER_PERCENT"),
        server_default=text(
            f"{PAYMENT_BASICS.get('DATA_MASTERCARD_WORLDWIDE_PARTNER_PERCENT')}"
        ),
        nullable=False,
    )

    data_mastercard_worldwide_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_MASTERCARD_WORLDWIDE_PARTNER_FIX"),
        server_default=text(
            f"{PAYMENT_BASICS.get('DATA_MASTERCARD_WORLDWIDE_PARTNER_FIX')}"
        ),
        nullable=False,
    )

    data_mastercard_worldwide_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_MASTERCARD_WORLDWIDE_SYSTEM_PERCENT"),
        server_default=text(
            f"{PAYMENT_BASICS.get('DATA_MASTERCARD_WORLDWIDE_SYSTEM_PERCENT')}"
        ),
        nullable=False,
    )

    data_mastercard_worldwide_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_MASTERCARD_WORLDWIDE_SYSTEM_FIX"),
        server_default=text(
            f"{PAYMENT_BASICS.get('DATA_MASTERCARD_WORLDWIDE_SYSTEM_FIX')}"
        ),
        nullable=False,
    )

    usdt_erc_20: Mapped[str | None] = mapped_column(String(200), nullable=True)

    usdt_erc_20_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_ERC20_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_ERC20_PARTNER_PERCENT')}"),
        nullable=False,
    )

    usdt_erc_20_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_ERC20_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_ERC20_PARTNER_FIX')}"),
        nullable=False,
    )

    usdt_erc_20_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_ERC20_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_ERC20_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    usdt_erc_20_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_ERC20_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_ERC20_SYSTEM_FIX')}"),
        nullable=False,
    )

    usdt_trc_20: Mapped[str | None] = mapped_column(String(200), nullable=True)

    usdt_trc_20_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_TRC20_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_TRC20_PARTNER_PERCENT')}"),
        nullable=False,
    )

    usdt_trc_20_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_TRC20_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_TRC20_PARTNER_FIX')}"),
        nullable=False,
    )

    usdt_trc_20_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_TRC20_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_TRC20_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    usdt_trc_20_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("USDT_TRC20_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('USDT_TRC20_SYSTEM_FIX')}"),
        nullable=False,
    )

    month_mc: Mapped[str | None] = mapped_column(String(2), nullable=True)

    year_mc: Mapped[str | None] = mapped_column(String(4), nullable=True)

    name_mc: Mapped[str | None] = mapped_column(String(100), nullable=True)

    surname_mc: Mapped[str | None] = mapped_column(String(100), nullable=True)

    birth_date_mc: Mapped[str | None] = mapped_column(String(20), nullable=True)

    country_code_mc: Mapped[str | None] = mapped_column(String(20), nullable=True)

    city_mc: Mapped[str | None] = mapped_column(String(100), nullable=True)

    address_mc: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_name: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_address: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_inn: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_ogrn: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_rs: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_bank: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_bank_inn: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_bank_bik: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_bank_ks: Mapped[str | None] = mapped_column(String(250), nullable=True)

    ip_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("IP_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('IP_PARTNER_PERCENT')}"),
        nullable=False,
    )

    ip_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("IP_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('IP_PARTNER_FIX')}"),
        nullable=False,
    )

    ip_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("IP_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('IP_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    ip_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("IP_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('IP_SYSTEM_FIX')}"),
        nullable=False,
    )

    oooru_name: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_address: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_inn: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_kpp: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_ogrn: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_rs: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_bank: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_bank_inn: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_bank_bik: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_bank_ks: Mapped[str | None] = mapped_column(String(250), nullable=True)

    oooru_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("OOORU_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('OOORU_PARTNER_PERCENT')}"),
        nullable=False,
    )

    oooru_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("OOORU_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('OOORU_PARTNER_FIX')}"),
        nullable=False,
    )

    oooru_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("OOORU_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('OOORU_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    oooru_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("OOORU_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('OOORU_SYSTEM_FIX')}"),
        nullable=False,
    )

    data_ua: Mapped[str | None] = mapped_column(Text, nullable=True)

    name_data_ua: Mapped[str | None] = mapped_column(String(100), nullable=True)

    surname_data_ua: Mapped[str | None] = mapped_column(String(100), nullable=True)

    data_ua_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_UA_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_UA_PARTNER_PERCENT')}"),
        nullable=False,
    )

    data_ua_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_UA_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_UA_PARTNER_FIX')}"),
        nullable=False,
    )

    data_ua_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_UA_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_UA_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    data_ua_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_UA_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_UA_SYSTEM_FIX')}"),
        nullable=False,
    )

    data_kz: Mapped[str | None] = mapped_column(Text, nullable=True)

    name_data_kz: Mapped[str | None] = mapped_column(String(100), nullable=True)

    surname_data_kz: Mapped[str | None] = mapped_column(String(100), nullable=True)

    data_kz_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_KZ_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_KZ_PARTNER_PERCENT')}"),
        nullable=False,
    )

    data_kz_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_KZ_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_KZ_PARTNER_FIX')}"),
        nullable=False,
    )

    data_kz_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_KZ_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_KZ_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    data_kz_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("DATA_KZ_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('DATA_KZ_SYSTEM_FIX')}"),
        nullable=False,
    )

    self_employed_tinkoff: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_tinkoff_fio: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_tinkoff_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_TINKOFF_PARTNER_PERCENT"),
        server_default=text(
            f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_TINKOFF_PARTNER_PERCENT')}"
        ),
        nullable=False,
    )

    self_employed_tinkoff_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_TINKOFF_PARTNER_FIX"),
        server_default=text(
            f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_TINKOFF_PARTNER_FIX')}"
        ),
        nullable=False,
    )

    self_employed_tinkoff_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_TINKOFF_SYSTEM_PERCENT"),
        server_default=text(
            f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_TINKOFF_SYSTEM_PERCENT')}"
        ),
        nullable=False,
    )

    self_employed_tinkoff_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_TINKOFF_SYSTEM_FIX"),
        server_default=text(
            f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_TINKOFF_SYSTEM_FIX')}"
        ),
        nullable=False,
    )

    self_employed: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_fio: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_phone: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_inn: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_bik: Mapped[str | None] = mapped_column(Text, nullable=True)

    self_employed_percent_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_PARTNER_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_PARTNER_PERCENT')}"),
        nullable=False,
    )

    self_employed_fix_partner: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_PARTNER_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_PARTNER_FIX')}"),
        nullable=False,
    )

    self_employed_percent_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_SYSTEM_PERCENT"),
        server_default=text(f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_SYSTEM_PERCENT')}"),
        nullable=False,
    )

    self_employed_fix_system: Mapped[float] = mapped_column(
        default=PAYMENT_BASICS.get("SELF_EMPLOYMENT_SYSTEM_FIX"),
        server_default=text(f"{PAYMENT_BASICS.get('SELF_EMPLOYMENT_SYSTEM_FIX')}"),
        nullable=False,
    )
