from pydantic import BaseModel, Field, ConfigDict

from typing import Annotated, Optional

from api_v4.models.partner.schemas import PartnerMin
from core.models.landing import StatusChoices, TypeChoices


class LandingBase(BaseModel):
    name: str | None = None
    offer_id: Annotated[int, Field(gt=0)] | None = None
    screenshot: str | None = None
    description: str | None = None
    status: Annotated[str, Optional[StatusChoices]] | None = None
    type: Annotated[str, Optional[TypeChoices]] | None = None
    landing_elements: Annotated[int, Field(gt=0)] | None = None
    private_partners: list["PartnerMin"] | None = None

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True


class LandingCreate(LandingBase):
    private_partners: list[Annotated[int, Field(gt=0)]] | None = None
    name: str
    offer_id: Annotated[int, Field(gt=0)]
    screenshot: str
    landing_elements: Annotated[int, Field(gt=0)] | None = None
    # land_elements: Mapped["LandingElement"] | None = None


class LandingUpdate(LandingBase):
    private_partners: list[Annotated[int, Field(gt=0)]] | None = None
    landing_elements: Annotated[int, Field(gt=0)] | None = None
    # land_elements: Mapped["LandingElement"] | None = None


class Landing(LandingBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class LandingRel(Landing):
    offer_id: Annotated[int, Field(gе=0)] | None = None
    # offer: Optional["OfferMin"] = None
    private_partners: list["PartnerMin"] | None = None
    elements: str | None = None
