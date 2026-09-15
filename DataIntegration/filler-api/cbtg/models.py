import decimal
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal

import pytz
from pydantic import Field, validator

from app.base import ORJSONModel


class SamrukTrdBuy(ORJSONModel):
    number: str = Field(alias="number")
    name: str = Field(alias="adName")


class GoszakupStatus(ORJSONModel):
    status_name: str = Field(alias="statusName")
    status_code: str = Field(alias="statusCode")

    def __init__(self, **data):
        status = data.pop("status")
        data["statusName"] = status["statusName"]
        data["statusCode"] = status["statusCode"]

        super().__init__(**data)


class GoszakupTradeMethod(ORJSONModel):
    trade_method_id: int = Field(alias="tradeMethodId")
    trade_method_name: str = Field(alias="tradeMethodName")

    def __init__(self, **data):
        status = data.pop("tradeMethod")
        data["tradeMethodName"] = status["tradeMethodName"]
        data["tradeMethodId"] = status["tradeMethodId"]

        super().__init__(**data)


class GoszakupBaseLot(ORJSONModel):
    number: str = Field(alias="lotNumber")
    name: str = Field(alias="lotName")
    amount: decimal.Decimal = Field(alias="amount")
    ad_number: str = Field(alias="adNumber")


class GoszakupLot(GoszakupBaseLot, GoszakupStatus):
    pass


class GoszakupBaseTrdBuy(ORJSONModel):
    number: str = Field(alias="adNumber")
    name: str = Field(alias="adName")
    beneficiary_bin: str = Field(alias="beneficiaryBin")
    beneficiary_name: str = Field(alias="beneficiaryName")
    repeat_start_date: datetime | None = Field(default=None, alias="repeatStartDate")
    repeat_end_date: datetime | None = Field(default=None, alias="repeatEndDate")
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    lots: list[GoszakupLot] = Field(alias="lots")
    trade_method_name: str = Field(default=None, alias="tradeMethodName")
    trade_method_code: str = Field(default=None, alias="tradeMethodCode")

    @validator("start_date", always=True)
    def validate_start_date(cls, value, values):
        repeat_start_date = values.get("repeat_start_date")
        if repeat_start_date is not None:
            return repeat_start_date
        return value

    @validator("end_date", always=True)
    def validate_end_date(cls, value, values):
        repeat_end_date = values.get("repeat_end_date")
        if repeat_end_date is not None:
            return repeat_end_date
        return value

    @validator("lots", pre=True)
    def validate_lots(cls, value):
        if value is None:
            return []
        return value

    @validator("trade_method_code", always=True, pre=True)
    def validate_trade_method_code(cls, value, values):
        mapping = {
            "Запрос ценовых предложений": "RequestForQuotations"
        }
        return mapping.get(values.get("trade_method_name"), "Other")


class GoszakupTrdBuy(GoszakupBaseTrdBuy, GoszakupStatus, GoszakupTradeMethod):
    pass


class GoszakupStatusResponse(ORJSONModel):
    status_code: str = Field(alias="statusCode")
    status_name: str = Field(alias="statusName")


class GoszakupLotResponse(GoszakupStatusResponse, GoszakupBaseLot):
    pass


class GoszakupTrdBuyResponse(GoszakupStatusResponse, GoszakupBaseTrdBuy):
    start_date: str = Field(default=None, alias="startDate")
    end_date: str = Field(default=None, alias="endDate")
    lots: list[GoszakupLotResponse] = Field(..., alias="lots")
    repeat_start_date: datetime = Field(default=None, exclude=True)
    repeat_end_date: datetime = Field(default=None, exclude=True)

    @validator("start_date", always=True, pre=True)
    def validate_start_date(cls, value, values):
        repeat_start_date = values.get("repeat_start_date")
        if repeat_start_date is not None:
            return repeat_start_date.strftime("%Y-%m-%d %H:%M:%S")
        return value.strftime("%Y-%m-%d %H:%M:%S")

    @validator("end_date", always=True, pre=True)
    def validate_end_date(cls, value, values):
        repeat_end_date = values.get("repeat_end_date")
        if repeat_end_date is not None:
            return repeat_end_date.strftime("%Y-%m-%d %H:%M:%S")
        return value.strftime("%Y-%m-%d %H:%M:%S")


class GoszakupTrdBuyResponseProd(GoszakupTrdBuyResponse):
    trade_method_name: str = Field(default=None, alias="tradeMethodName", exclude=True)
    trade_method_code: str = Field(default=None, alias="tradeMethodCode", exclude=True)


class HealthCheckResponse(ORJSONModel):
    status_code: str = Field(None, alias="statusCode")
    status_name: str | None = Field(None, alias="statusName")


class SamrukLot(ORJSONModel):
    id: str = Field(alias="id")
    name: str = Field(alias="nameRu")
    amount: decimal.Decimal = Field(alias="sumTruNoNds")
    ad_number: str = Field(alias="adNumber")
    status_code: str = Field(alias="lotStatus")


class SamrukLotResponse(ORJSONModel):
    id: str = Field(alias="lotNumber")
    name: str = Field(alias="lotName")
    amount: decimal.Decimal = Field(alias="amount")
    ad_number: str = Field(alias="adNumber")
    status_code: str = Field(alias="statusCode")
    status_name: str = Field(default="", alias="statusName")

    @validator("status_name", always=True)
    def validate_status_name(cls, value, values):
        lot_status_names: dict[str, str] = {
            "PublishedBidAccept": "Опубликован (прием заявок)",
        }
        status_code = values["status_code"]

        return lot_status_names.get(status_code, value)

    @validator("status_code")
    def validate_status_code(cls, value):
        lot_statuses: dict[str, str] = {
            "PUBLISHED": "PublishedBidAccept"
        }
        return lot_statuses.get(value, value)


class SamrukAd(ORJSONModel):
    number: str = Field(alias="number")
    name: str = Field(alias="nameRu")
    beneficiary_bin: str = Field(alias="beneficiaryBin")
    beneficiary_name: str = Field(alias="beneficiaryName")
    start_date: datetime | None = Field(alias="acceptanceBeginDateTime")
    end_date: datetime | None = Field(alias="acceptanceEndDateTime")
    lots: list[SamrukLot] = Field(..., alias="lots")
    status_code: str = Field(alias="advertStatus")
    file_uid: str | None = Field(alias="tenderDocFileUid")

    @validator("start_date", "end_date", pre=True)
    def validate_dates(cls, value):
        if value is None:
            return
        value = pytz.timezone("Asia/Almaty").localize(
            datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f%z').astimezone(
                timezone(timedelta(hours=6))
            ).replace(tzinfo=None)
        )
        return value


class SamrukAdResponse(ORJSONModel):
    number: str = Field(alias="adNumber")
    name: str = Field(alias="adName")
    beneficiary_bin: str = Field(alias="beneficiaryBin")
    beneficiary_name: str = Field(alias="beneficiaryName")
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    lots: list[SamrukLotResponse] = Field(..., alias="lots")
    status_code: str = Field(alias="statusCode")
    status_name: str = Field(default="", alias="statusName")
    file_uid: str | None = Field(alias="tenderDocFileUid")

    @validator("start_date", "end_date", pre=True, always=True)
    def validate_dates(cls, value):
        date_pattern = "%Y-%m-%d %H:%M:%S"
        if value is None:
            return
        return datetime.strftime(value, date_pattern)

    @validator("status_name", always=True)
    def validate_status_name(cls, value, values):
        ad_status_names: dict[str, str] = {
            "PublishedOrderTaking": "Опубликовано (прием заявок)",
        }
        status_code = values["status_code"]

        return ad_status_names.get(status_code, value)

    @validator("status_code")
    def validate_status_code(cls, value):
        ad_statuses: dict[str, str] = {
            "PUBLISHED": "PublishedOrderTaking",
        }
        return ad_statuses.get(value, value)


class SkPharmacyLot(ORJSONModel):
    id: str = Field(alias="id")
    name: str = Field(alias="nameRu")
    amount: str = Field(alias="sumTruNoNds")
    ad_number: str = Field(alias="adNumber")
    status_name: str = Field(alias="lotStatus")

    @validator("amount", always=True)
    def validate_amount(cls, value):
        amount_wo_whitespace = value.replace(" ", "").replace(",", "")
        value = decimal.Decimal(amount_wo_whitespace)
        return value


class SkPharmacyLotResponse(ORJSONModel):
    id: str = Field(alias="lotNumber")
    name: str = Field(alias="lotName")
    amount: decimal.Decimal = Field(alias="amount")
    ad_number: str = Field(alias="adNumber")
    status_name: str = Field(alias="statusName")
    status_code: str = Field(default="", alias="statusCode")

    @validator("status_code", always=True)
    def validate_status_name(cls, value, values):
        lot_status_names: dict[str, str] = {
            "Опубликован (прием заявок)": "PublishedOrderTaking",
            "Опубликован (дополнение заявок)": "PublishedAdditionDemands"
        }
        status_name = values["status_name"]

        return lot_status_names.get(status_name, value)


class SkPharmacyAd(ORJSONModel):
    number: str = Field(alias="number")
    name: str = Field(alias="nameRu")
    beneficiary_bin: str = Field(alias="beneficiaryBin")
    beneficiary_name: str = Field(alias="beneficiaryName")
    #ad_method: str = Field(alias="adMethod")
    repeat_start_date: datetime | None = Field(default=None, alias="repeatStartDate")
    repeat_end_date: datetime | None = Field(default=None, alias="repeatEndDate")
    start_date: datetime | None = Field(alias="acceptanceBeginDateTime")
    end_date: datetime | None = Field(alias="acceptanceEndDateTime")
    lots: list[SkPharmacyLot] = Field(..., alias="lots")
    status_name: str = Field(alias="advertStatus")

    @validator("start_date", "end_date", pre=True)
    def validate_dates(cls, value):
        if value is None:
            return
        value = datetime.fromisoformat(value)
        return value

    @validator("start_date", always=True)
    def validate_start_date(cls, value, values):
        repeat_start_date = values.get("repeat_start_date")
        if repeat_start_date:
            return repeat_start_date
        return value

    @validator("end_date", always=True)
    def validate_end_date(cls, value, values):
        repeat_end_date = values.get("repeat_end_date")
        if repeat_end_date:
            return repeat_end_date
        return value

    @validator("lots", pre=True)
    def validate_lots(cls, value):
        if value is None:
            return []
        return value


class SkPharmacyAdResponse(ORJSONModel):
    number: str = Field(alias="adNumber")
    name: str = Field(alias="adName")
    beneficiary_bin: str = Field(alias="beneficiaryBin")
    beneficiary_name: str = Field(alias="beneficiaryName")
    #ad_method: str = Field(alias="adMethod")
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    lots: list[SkPharmacyLotResponse] = Field(..., alias="lots")
    status_name: str = Field(alias="statusName")
    status_code: str = Field(default="", alias="statusCode")

    @validator("start_date", "end_date", pre=True, always=True)
    def validate_dates(cls, value):
        date_pattern = "%Y-%m-%d %H:%M:%S"
        if value is None:
            return
        return datetime.strftime(value, date_pattern)

    @validator("status_code", always=True)
    def validate_status_name(cls, value, values):
        lot_status_names: dict[str, str] = {
            "Опубликовано (прием заявок)": "PublishedOrderTaking",
            "Опубликовано (дополнение заявок)": "PublishedAdditionDemands"
        }
        status_name = values["status_name"]
        return lot_status_names.get(status_name, value)
