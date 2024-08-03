from pydantic import BaseModel, ConfigDict, Field
from core.models.invoice import TypeChoices
from typing import Annotated
from datetime import datetime


class InvoiceBase(BaseModel):
    operation_type: TypeChoices
    operation_id: Annotated[int, Field(gt=0)]
    create_date: datetime | None = None
    n_subscription_id: Annotated[int, Field(ge=0)] | None = None
    n_client_id: Annotated[int, Field(ge=0)] | None = None
    n_host_id: Annotated[int, Field(ge=0)] | None = None
    n_partner_id: Annotated[int, Field(ge=0)] | None = None
    n_stream_id: Annotated[int, Field(ge=0)] | None = None
    n_offer_id: Annotated[int, Field(ge=0)] | None = None
    n_landing_id: Annotated[int, Field(ge=0)] | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
