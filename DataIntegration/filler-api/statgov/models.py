from datetime import date, datetime

from pydantic import BaseModel, Field, validator


class RequestBody(BaseModel):
    biniin: str = Field(
        ...,
        regex=r"^[\d]{12}$",
        title="БИН/ИИН клиента",
        alias="biniin",
    )  # RegEx checks if `biniin` contains exactly 12 numbers

    class Config:
        allow_population_by_field_name = True


class CompanyInformation(BaseModel):
    bin: str | None = Field(
        ..., title="БИН/ИИН клиента", alias="bin"
    )  # regex=r'^[\d]{12}$'
    name: str | None = Field(..., alias="name")
    register_date: str | None = Field(..., alias="registerDate")
    oked_code: str | None = Field(..., alias="okedCode")
    oked_name: str | None = Field(..., alias="okedName")
    second_okeds: str | None = Field(..., alias="secondOkeds")
    krp_code: str | None = Field(..., alias="krpCode")
    krp_name: str | None = Field(..., alias="krpName")
    kato_code: str | None = Field(..., alias="katoCode")
    kato_description: str | None = Field(..., alias="katoDescription")
    legal_address: str | None = Field(..., alias="legalAddress")
    owner: str | None = Field(..., alias="owner")
    period_code: str | None = Field(..., alias="periodCode")
    period_date: date | None = Field(..., alias="periodDate")

    class Config:
        allow_population_by_field_name = True


class CompanyInformationAPI(CompanyInformation):
    @validator(
        "register_date",
        always=True,
        pre=True,
    )
    def reformat_date(cls, v):
        return datetime.strptime(v, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d")
