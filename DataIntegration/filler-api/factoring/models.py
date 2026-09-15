import logging
from datetime import date, datetime

import pytz
from pydantic import Field, validator

from app.base import ORJSONModel
from app.models import apply_conversion

logger = logging.getLogger()


RESPONSE_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
RESPONSE_DATE_FORMAT = "%Y-%m-%d"


class SamrukFactoring(ORJSONModel):
    contract_id: int = Field(alias="contract_id")
    contract_number: str = Field(alias="contract_number")
    contract_status: str = Field(alias="contract_status")
    contract_sum_nds: str = Field(alias="contract_sum_nds")
    contract_sum_no_nds: str = Field(alias="contract_sum_no_nds")
    execution_sum_nds: str | None = Field(alias="execution_sum_nds")
    execution_sum_no_nds: str | None = Field(alias="execution_sum_no_nds")

    supplier_name_kz: str | None = Field(alias="supplier_name_kz")
    supplier_name_ru: str | None = Field(alias="supplier_name_ru")
    supplier_bin_iin: str = Field(alias="supplier_bin_iin")

    customer_name_kz: str | None = Field(alias="customer_name_kz")
    customer_name_ru: str | None = Field(alias="customer_name_ru")
    customer_bin_iin: str = Field(alias="customer_bin_iin")

    customer_bik: str = Field(alias="customer_bik")
    customer_iik: str = Field(alias="customer_iik")
    supplier_bik: str = Field(alias="supplier_bik")
    supplier_iik: str = Field(alias="supplier_iik")
    act_sum: str | None = Field(alias="act_sum")
    act_last_date: str | None = Field(alias="act_last_date")
    act_status: str | None = Field(alias="act_status")


class LocalizedFactoringAttr(ORJSONModel):
    supplier_name: str | None = Field(alias="supplierName")
    customer_name: str | None = Field(alias="customerName")


class Factoring(ORJSONModel):
    contract_id: str = Field(alias="contractId")
    contract_number: str = Field(alias="contractNumber")
    contract_status: str = Field(alias="contractStatus")
    contract_amount: str = Field(alias="contractAmount")
    contract_amount_without_nds: str = Field(alias="contractAmountWithoutNds")
    execution_amount: str | None = Field(alias="executionAmount")
    execution_amount_without_nds: str | None = Field(alias="executionAmountWithoutNds")

    supplier_bin_iin: str = Field(alias="supplierBinIin")
    customer_bin_iin: str = Field(alias="customerBinIin")
    customer_bik: str = Field(alias="customerBik")
    customer_iik: str = Field(alias="customerIik")
    supplier_bik: str = Field(alias="supplierBik")
    supplier_iik: str = Field(alias="supplierIik")

    ru: LocalizedFactoringAttr = Field(default=None, alias="ru")
    kk: LocalizedFactoringAttr = Field(default=None, alias="kk")

    act_sum: str | None = Field(alias="actSum")
    act_last_date: datetime | None = Field(alias="actLastDate")
    act_status: str | None = Field(alias="actStatus")

    class Config:
        allow_population_by_field_name = True


class FactoringResponseItem(ORJSONModel):
    contract_id: str = Field(alias="contractId")
    contract_number: str = Field(alias="contractNumber")
    contract_status: str = Field(alias="contractStatus")
    contract_amount: str = Field(alias="contractAmount")
    contract_amount_without_nds: str = Field(alias="contractAmountWithoutNds")
    execution_amount: str | None = Field(alias="executionAmount")
    execution_amount_without_nds: str | None = Field(alias="executionAmountWithoutNds")

    customer_bin_iin: str = Field(alias="customerBinIin")
    customer_bik: str = Field(alias="customerBik")
    customer_iik: str = Field(alias="customerIik")
    supplier_bin_iin: str = Field(alias="supplierBinIin")
    supplier_bik: str = Field(alias="supplierBik")
    supplier_iik: str = Field(alias="supplierIik")

    ru: LocalizedFactoringAttr = Field(default=None, alias="ru")
    kk: LocalizedFactoringAttr = Field(default=None, alias="kk")

    act_sum: str | None = Field(alias="actSum")
    act_last_date: str | None = Field(alias="actLastDate")
    act_status: str | None = Field(alias="actStatus")

    @validator("act_last_date", pre=False, always=True)
    def validate_dates(cls, value: str):
        datetime.strptime(value, RESPONSE_DATETIME_FORMAT)
        return value

    class Config:
        allow_population_by_field_name = True


class FactoringResponse(ORJSONModel):
    items: list[FactoringResponseItem] = Field(alias="items")


@apply_conversion.register
def _(source: SamrukFactoring, target):
    current_zone = pytz.timezone("Asia/Almaty")
    format_time = lambda x: x[:-2] + ':' + x[-2:] if (x[-5] in ['+', '-']) and (':' not in x[-3:]) else x

    match target:
        case type() as cls if issubclass(cls, Factoring):
            act_last_date = datetime.fromisoformat(format_time(source.act_last_date))

            return Factoring(
                contractId=str(source.contract_id),
                contractNumber=source.contract_number,
                contractStatus=source.contract_status,
                contractAmount=source.contract_sum_nds,
                contractAmountWithoutNds=source.contract_sum_no_nds,
                executionAmount=source.execution_sum_nds,
                executionAmountWithoutNds=source.execution_sum_no_nds,

                customerBinIin=source.customer_bin_iin,
                customerBik=source.customer_bik,
                customerIik=source.customer_iik,

                supplierBinIin=source.supplier_bin_iin,
                supplierBik=source.supplier_bik,
                supplierIik=source.supplier_iik,

                ru=LocalizedFactoringAttr(
                    supplierName=source.supplier_name_ru,
                    customerName=source.customer_name_ru,
                ),
                kk=LocalizedFactoringAttr(
                    supplierName=source.supplier_name_kz,
                    customerName=source.customer_name_kz,
                ),

                actSum=source.act_sum,
                actLastDate=act_last_date.astimezone(current_zone),
                actStatus=source.act_status,
            )
        case type():
            raise TypeError
        case _:
            raise TypeError


@apply_conversion.register
def _(source: Factoring, target):
    match target:
        case type() as cls if issubclass(cls, FactoringResponseItem):
            return FactoringResponseItem(
                contractId=source.contract_id,
                contractNumber=source.contract_number,
                contractStatus=source.contract_status,
                contractAmount=source.contract_amount,
                contractAmountWithoutNds=source.contract_amount_without_nds,
                executionAmount=source.execution_amount,
                executionAmountWithoutNds=source.execution_amount_without_nds,

                customerBinIin=source.customer_bin_iin,
                customerBik=source.customer_bik,
                customerIik=source.customer_iik,

                supplierBinIin=source.supplier_bin_iin,
                supplierBik=source.supplier_bik,
                supplierIik=source.supplier_iik,

                ru=LocalizedFactoringAttr(
                    supplierName=source.ru.supplier_name,
                    customerName=source.ru.customer_name,
                ),
                kk=LocalizedFactoringAttr(
                    supplierName=source.kk.supplier_name,
                    customerName=source.kk.customer_name,
                ),

                actSum=source.act_sum,
                actLastDate=source.act_last_date.strftime(RESPONSE_DATETIME_FORMAT),
                actStatus=source.act_status,
            )
        case type():
            raise TypeError
        case _:
            raise TypeError


class SamrukContract(ORJSONModel):
    id: int = Field(alias="id")
    number: str = Field(alias="contract_number")
    items_name_kk: str | None = Field(alias="contract_items_name_kk")
    items_name_ru: str | None = Field(alias="contract_items_name_ru")
    advert_id: int = Field(alias="advert_id")
    supplier_bin: str = Field(alias="supplier_bin")
    supplier_name: str = Field(alias="supplier_name")
    supplier_name_kk: str = Field(alias="supplier_name_kk")
    sum_nds: str = Field(alias="sum_nds")
    sum_no_nds: str = Field(alias="sum_no_nds")
    contract_date_time: str = Field(alias="contract_date_time")
    contract_end_time: str = Field(alias="contract_end_time")
    customer_bin: str = Field(alias="customer_bin")
    customer_name: str = Field(alias="customer_name")
    customer_name_kk: str = Field(alias="customer_name_kk")
    status: str = Field(alias="status")
    advance_refund_percent: str | None = Field(alias="advance_refund_percent")
    contract_execution_percent: str | None = Field(alias="contract_execution_percent")


class LocalizedContractAttr(ORJSONModel):
    supplier_name: str | None = Field(alias="supplierName")
    customer_name: str | None = Field(alias="customerName")
    items_name: str | None = Field(alias="itemsName")


class Contract(ORJSONModel):
    id: str = Field(alias="id")
    number: str = Field(alias="number")
    advert_id: str = Field(alias="advertId")
    supplier_bin_iin: str = Field(alias="supplierBinIin")
    amount: str = Field(alias="amount")
    amount_without_nds: str = Field(alias="amountWithoutNds")
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    customer_bin_iin: str = Field(alias="customerBinIin")

    ru: LocalizedContractAttr | None = Field(default=None, alias="ru")
    kk: LocalizedContractAttr | None = Field(default=None, alias="kk")
    status: str = Field(alias="status")

    class Config:
        allow_population_by_field_name = True


class ContractResponse(ORJSONModel):
    contract_id: str = Field(alias="contractId")
    contract_number: str = Field(alias="contractNumber")
    ad_id: str = Field(alias="adId")
    supplier_bin_iin: str = Field(alias="supplierBinIin")
    contract_amount: str = Field(alias="contractAmount")
    contract_amount_without_nds: str = Field(alias="contractAmountWithoutNds")
    contract_start_date: date = Field(alias="contractStartDate")
    contract_end_date: date = Field(alias="contractEndDate")
    customer_bin_iin: str = Field(alias="customerBinIin")

    ru: LocalizedContractAttr | None = Field(default=None, alias="ru")
    kk: LocalizedContractAttr | None = Field(default=None, alias="kk")
    contract_status: str = Field(alias="contractStatus")

    @validator("contract_start_date", "contract_end_date", pre=True, always=True)
    def validate_dates(cls, value):
        if value is None:
            return
        value = datetime.strftime(value, "%Y-%m-%d")
        return value

    class Config:
        allow_population_by_field_name = True


@apply_conversion.register
def _(source: SamrukContract, target):
    current_zone = pytz.timezone("Asia/Almaty")
    format_time = lambda x: x[:-2] + ':' + x[-2:] if (x[-5] in ['+', '-']) and (':' not in x[-3:]) else x

    match target:
        case type() as cls if issubclass(cls, Contract):
            source_start_time = datetime.fromisoformat(format_time(source.contract_date_time))
            source_end_time = datetime.fromisoformat(format_time(source.contract_end_time))

            return Contract(
                id=str(source.id),
                number=source.number,
                advertId=str(source.advert_id),
                supplierBinIin=source.supplier_bin,
                amount=source.sum_nds,
                amountWithoutNds=source.sum_no_nds,
                startDate=source_start_time.astimezone(current_zone),
                endDate=source_end_time.astimezone(current_zone),
                customerBinIin=source.customer_bin,
                ru=LocalizedContractAttr(
                    supplierName=source.supplier_name,
                    customerName=source.customer_name,
                    itemsName=source.items_name_ru,
                ),
                kk=LocalizedContractAttr(
                    supplierName=source.supplier_name_kk,
                    customerName=source.customer_name_kk,
                    itemsName=source.items_name_kk,
                ),
                status=source.status,
            )
        case type():
            raise TypeError
        case _:
            raise TypeError


@apply_conversion.register
def _(source: Contract, target):
    match target:
        case type() as cls if issubclass(cls, ContractResponse):
            return ContractResponse(
                contractId=source.id,
                contractNumber=source.number,
                adId=source.advert_id,
                supplierBinIin=source.supplier_bin_iin,
                contractAmount=source.amount,
                contractAmountWithoutNds=source.amount_without_nds,
                contractStartDate=source.start_date,
                contractEndDate=source.end_date,
                customerBinIin=source.customer_bin_iin,
                ru=LocalizedContractAttr(
                    supplierName=source.ru.supplier_name,
                    customerName=source.ru.customer_name,
                    itemsName=source.ru.items_name,
                ),
                kk=LocalizedContractAttr(
                    supplierName=source.kk.supplier_name,
                    customerName=source.kk.customer_name,
                    itemsName=source.kk.items_name,
                ),
                contractStatus=source.status,
            )
        case type():
            raise TypeError
        case _:
            raise TypeError
