from datetime import datetime
from enum import Enum

from pydantic import Field, validator

from app.base import ORJSONModel
from app.exceptions import ValidationError


class SystemTypes(str, Enum):
    onlinebank = "onlinebank"


class Offer(ORJSONModel):
    offer_id: str = Field(..., alias="offerId")
    product_code: str = Field(..., alias="productCode")
    product_direction: str = Field(..., alias="productDirection")
    roles: list[str] = Field(None, alias="roles")
    cacheperiod: datetime | None = Field(..., alias="cachePeriod")
    validity: datetime | None = Field(..., alias="validity")

    @validator("product_direction", always=True, pre=True)
    def _validate_product_direction(cls, value: str):
        return value.rstrip()

    @validator("roles", always=True, pre=True)
    def roles_to_list(cls, values):
        if values is None:
            return []

        if isinstance(values, str):
            return values.split(", ")

        if isinstance(values, list):
            return values

        raise ValidationError("roles must be a list")


class GetOfferResponse(ORJSONModel):
    data: list[Offer] = []


class OfferInterest(ORJSONModel):
    offer_id: int = Field(..., alias="offerId")
    role: str = Field(..., alias="role")
    action_date: str | datetime = Field(..., alias="actionDateTime")

    @validator("action_date", pre=True)
    def validate_date(cls, value):
        try:
            return datetime.fromisoformat(value).isoformat()
        except ValueError:
            raise ValidationError("Not valid date iso format")


class ActivatedOffers(ORJSONModel):
    type: str
    data: list[str]
