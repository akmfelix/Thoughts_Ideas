from datetime import date
from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


class SystemTypes(str, Enum):
    ocrm = "ocrm"


class MVPIncome(BaseModel):
    biniin: str | None = Field(..., alias="biniin")
    client_code: str | None = Field(..., alias="client_code")
    product_category_id: UUID = Field(..., alias="product_category_id")
    product_code: str = Field(..., alias="product_code")
    date_by_month: date = Field(..., alias="date_by_month")
    income: int = Field(..., alias="income")


class MVPFuture(BaseModel):
    biniin: str | None = Field(..., alias="biniin")
    client_code: str | None = Field(..., alias="client_code")
    product_category_id: UUID = Field(..., alias="product_category_id")
    product_code: str = Field(..., alias="product_code")
    future: int = Field(..., alias="future")


class MVPUserAttributes(BaseModel):
    is_high_profit_client: Decimal = Field(None, alias="isHighProfitClient")

    class Config:
        allow_population_by_field_name = True


class MVPProduct(BaseModel):
    future: int = None
    incomes: dict[str, int] = None


MVPResponse = dict
