from pydantic import BaseModel, Field, ConfigDict

from core.models.prelanding import TypeChoices, StatusChoices

from typing import Annotated, Optional

from api_v4.models.partner.schemas import PartnerMin


class PrelandingBase(BaseModel):
    name: str | None = None
    offer_id: Annotated[int, Field(gt=0)] | None = None
    screenshot: str | None = None
    description: str | None = None
    status: Annotated[str, Optional[StatusChoices]] | None = None
    type: Annotated[str, Optional[TypeChoices]] | None = None
    private_partners: list["PartnerMin"] | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class PrelandingCreate(PrelandingBase):
    name: str
    screenshot: str
    offer_id: Annotated[int, Field(gt=0)]
    private_partners: list[Annotated[int, Field(gt=0)]] | None = None


class PrelandingUpdate(PrelandingBase):
    private_partners: list[Annotated[int, Field(gt=0)]] | None = None


class Prelanding(PrelandingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class PrelandingRel(Prelanding):
    offer_id: Annotated[int, Field(gt=0)] | None = None
    # offer: Optional["OfferMin"] = None
    private_partners: list["PartnerMin"] | None = None
