import json
from datetime import date

from pydantic import Field, validator

from app.base import ORJSONModel


class Turnover(ORJSONModel):
    period: date
    opening_balance: str = Field(..., alias="openingBalance")
    inflow: str = Field(..., alias="inflow") # credit
    outflow: str = Field(..., alias="outflow") # debit
    closing_balance: str = Field(..., alias="closingBalance")


class Reference(ORJSONModel):
    max_date: str | None = Field(None, alias="maxDate")
    turnovers: list[Turnover] = Field(default_factory=list, alias="turnovers")

    @validator("turnovers", pre=True)
    @classmethod
    def parse_turnovers(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            return json.loads(v)
        return v
