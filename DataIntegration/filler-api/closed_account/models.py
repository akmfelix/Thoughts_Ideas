from datetime import date

from pydantic import Field

from app.base import ORJSONModel


class ClosedAccount(ORJSONModel):
    account_number: str = Field(..., alias="accountNumber")
    closed_date: date = Field(..., alias="closedDate")
    acc_currency: str = Field(..., alias="accCurrency")


class ClosedAccountByBin(ORJSONModel):
    account_number: str = Field(..., alias="accountNumber")
    closed_date: date = Field(..., alias="closedDate")
    acc_currency: str = Field(..., alias="accCurrency")
    acc_type: str | None = Field(default=None, alias="accType")
    acc_type_name: str | None = Field(default=None, alias="accTypeName")


class ClosedAccountResponse(ORJSONModel):
    account: ClosedAccount | None = Field(default=None, alias="account")


class ClosedAccountsResponse(ORJSONModel):
    accounts: list[ClosedAccountByBin] = Field(default_factory=list, alias="accounts")
