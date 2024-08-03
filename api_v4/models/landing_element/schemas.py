from pydantic import BaseModel, ConfigDict


class LandingElementBase(BaseModel):
    elements: str | None = None


class LandingElementCreate(LandingElementBase):
    pass


class LandingElementUpdate(LandingElementBase):
    pass


class LandingElement(LandingElementBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
