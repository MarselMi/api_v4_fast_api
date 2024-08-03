from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict
from typing import Annotated, Optional
from core.models.promo import TypeChoices, StatusChoices, ViewChoices


class BasePromo(BaseModel):
    name: Annotated[str, MaxLen(64)] | None = None
    type: Annotated[str, Optional["TypeChoices"], MaxLen(20)] | None = None
    status: Annotated[str, Optional["StatusChoices"], MaxLen(5)] | None = None
    view: Annotated[str, Optional["ViewChoices"], MaxLen(10)] | None = None
    js_src: Annotated[str, MaxLen(255)] | None = None
    js: str | None = None


class Promo(BasePromo):
    model_config = ConfigDict(from_attributes=True)

    id: int
