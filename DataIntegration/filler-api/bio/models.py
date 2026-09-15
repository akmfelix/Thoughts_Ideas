import math
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_CEILING

import pytz
from dateutil import parser
from pydantic import Field, root_validator, validator

from app.base import ORJSONModel
from app.models import apply_conversion


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
    contract_execution_percent: str | None = Field(alias="contractExecutionPercent")

    ru: LocalizedContractAttr | None = Field(default=None, alias="ru")
    kk: LocalizedContractAttr | None = Field(default=None, alias="kk")
    status: str = Field(alias="status")

    class Config:
        allow_population_by_field_name = True


class ContractResponse(ORJSONModel):
    contract_id: str = Field(alias="contractId")
    contract_number: str = Field(alias="contractNumber")
    ad_id: str = Field(alias="adId")
    guarantee_amount: Decimal = Field(alias="guaranteeAmount")
    supplier_bin_iin: str = Field(alias="supplierBinIin")
    supplier_name: str = Field(alias="supplierName")
    contract_description: str = Field(alias="contractDescription")
    contract_amount: Decimal = Field(alias="contractAmount")
    contract_amount_without_nds: Decimal = Field(alias="contractAmountWithoutNds")
    contract_start_date: date = Field(alias="contractStartDate")
    contract_end_date: date = Field(alias="contractEndDate")
    customer_bin_iin: str = Field(alias="customerBinIin")
    customer_name: str = Field(alias="customerName")
    guarantee_percent: str = Field(alias="guaranteePercent")
    contract_status: str = Field(alias="contractStatus")
    contract_type: int = Field(alias="contractType")
    contract_type_year: int = Field(alias="contractTypeYear")

    @validator(
        "guarantee_amount",
        "contract_amount",
        "contract_amount_without_nds",
        pre=False,
        always=True
    )
    def round_guarantee_amount(cls, value: Decimal):
        return value.quantize(Decimal("0.01"), rounding=ROUND_CEILING)

    @validator("contract_start_date", "contract_end_date", pre=True, always=True)
    def validate_dates(cls, value):
        if value is None:
            return
        value = datetime.strftime(value, "%Y-%m-%d")
        return value

    class Config:
        allow_population_by_field_name = True


class ContractEnforcement(ORJSONModel):
    not_required: int = Field(default=0, alias="absenceSecurityPerformanceContract")
    money_transfer_3percent: int = Field(default=0, alias="securityDepositTotalAmountContract")
    guarantee_dumping: int = Field(default=0, alias="bankGuaranteeAmountInAccordanceLaw26")
    cash_dumping: int = Field(default=0, alias="cashGuaranteeAmountInAccordanceLaw26")
    wallet_3percent: int = Field(default=0, alias="ewalletCollateralMoney3percentContractAmount")
    wallet_dumping: int = Field(default=0, alias="ewalletMoneyAmountInAccordanceLaw26")
    guarantee_prepayment: int = Field(default=0, alias="bankGuaranteeAmountInAdvanceUnderContract")
    insurance_3percent: int = Field(
        default=0, alias="civilLiabilityInsurance3percentTotalContractAmount"
    )
    guarantee_3percent: int = Field(default=0, alias="bankGuarantee3percentTotalContractAmount")
    attachment_status: str = Field(default=None, alias="attachmentStatus")


class TreasuryPay(ORJSONModel):
    bik_supplier: str | None = Field(alias="bikSupplier")
    pay_amount: Decimal | None = Field(alias="payAmount")
    pay_date: datetime | None = Field(alias="payDate")
    pay_quantity: int = Field(default=1, alias="payQuantity")


class ReceivedPayment(ORJSONModel):
    bik_supplier: str | None = Field(alias="bikSupplier")
    pay_amount: Decimal | None = Field(alias="payAmount")
    pay_month: str | None = Field(alias="payMonth")
    pay_quantity: int = Field(default=1, alias="payQuantity")


class ReceivedPayments(ORJSONModel):
    bin: str = Field(..., alias="bin")
    received_payments: list[ReceivedPayment] = Field(alias="receivedPayments")


class Page(ORJSONModel):
    limit_page: int = Field(..., alias="limitPage")
    total_count: int = Field(..., alias="totalCount")
    has_next_page: bool = Field(..., alias="hasNextPage")
    last_id: int = Field(..., alias="lastId")


class BioContract(ORJSONModel):
    id: int = Field(..., alias="id")
    contract_number: str = Field(..., alias="contractNumber")
    contract_type: int = Field(..., alias="contractType")
    contract_year_type: int = Field(..., alias="contractYearType")
    sign_date: str = Field(..., alias="signDate")
    ad_number: str = Field(..., alias="adNumber")
    ad_name_ru: str = Field(..., alias="adName")
    customer_bin_iin: str = Field("", alias="customerBinIin")
    customer_name_ru: str = Field("", alias="customerName")
    contract_sum: Decimal = Field(..., alias="contractSum")
    contract_sum_wnds: Decimal = Field(..., alias="contractSumWnds")
    fakt_sum: Decimal = Field(..., alias="faktSum")
    fakt_sum_wnds: Decimal = Field(..., alias="faktSumWnds")
    trade_methods_name_ru: str = Field("", alias="tradeMethodsName")
    trade_methods_code: str = Field("", alias="tradeMethodsCode")
    status_name: str = Field("", alias="statusName")

    @root_validator(pre=True)
    def validate_customer_bin(cls, values):

        customer = values.get("customer", None)
        if isinstance(customer, dict):
            values["customerBinIin"] = (
                customer.get("bin") if customer.get("bin", "") != "" else customer.get("iin", "")
            )
            values["customerName"] = customer.get("nameRu")

        trade_methods = values.get("FaktTradeMethods", None)
        if isinstance(trade_methods, dict):
            values["tradeMethodsName"] = trade_methods.get("nameRu")
            values["tradeMethodsCode"] = trade_methods.get("symbolCode")

        contract_status = values.get("RefContractStatus", None)
        if isinstance(contract_status, dict):
            values["statusName"] = contract_status.get("nameRu")

        return values


class BioContractResponse(ORJSONModel):
    contracts: list[BioContract] = []
    current_id: int = Field(..., alias="currentId")
    next_id: int = Field(..., alias="nextId")


class Guarantee(ORJSONModel):
    contract_number: str | None = Field(None, alias="contractNumber")
    customer_bin_iin: str | None = Field(None, alias="customerBinIin")
    customer_name: str | None = Field(None, alias="customerName")
    contract_subject: str | None = Field(None, alias="contractSubjectRu")
    # contract_subject_kz: str | None = Field(None, alias="contractSubjectKz")
    sign_date: str | None = Field(None, alias="contractSignDate")
    plan_execution_date: str | None = Field(None, alias="planExecDate")
    fakt_execution_date: str | None = Field(None, alias="faktExecDate")
    ec_end_date: str | None = Field(None, alias="ecEndDate")
    contract_amount_wnds: str | None = Field(None, alias="contractAmountWnds")
    guarantee_amount: str | None = Field(None, alias="guaranteeAmount")
    contract_file_path: str | None = Field(None, alias="contractFilePath")

    @root_validator(pre=True)
    def map_base_nested_data(cls, values):
        if not isinstance(values, dict):
            return values

        customer = values.get("Customer")
        if isinstance(customer, dict):
            values["customerBinIin"] = customer.get("customerBin") or customer.get("bin") or ""
            values["customerName"] = (
                customer.get("customerNameRu") or customer.get("customerFullNameRu") or ""
            )

        file = values.get("File")
        if isinstance(file, dict):
            values["contractFilePath"] = file.get("contractFilePath") or file.get("filePath")

        return values

    @validator("sign_date", "plan_execution_date", "fakt_execution_date", "ec_end_date")
    def truncate_time(cls, v: str | None):
        if v is not None:
            return parser.parse(v).date()


class BlankGuaranteeContract(Guarantee):
    id: int = Field(None, alias="id")
    contract_type: str | None = Field(None, alias="contractType")
    purchase_type: str | None = Field(None, alias="purchaseType")
    contract_period: str | None = Field(None, alias="contractPeriod")
    contract_end_date: str | None = Field(None, alias="contractEndDate")
    supplier_name: str | None = Field(None, alias="supplierName")
    supplier_bin_iin: str | None = Field(None, alias="supplierBinIin")

    @root_validator(pre=True)
    def map_blank_specific_data(cls, values):
        if not isinstance(values, dict):
            return values

        values = super().map_base_nested_data(values)

        ref_type = values.get("RefContractType")
        if isinstance(ref_type, dict):
            values["contractType"] = ref_type.get("contractType") or ref_type.get("nameRu")

        ref_year_type = values.get("RefContractYearType")
        if isinstance(ref_year_type, dict):
            values["purchaseType"] = ref_year_type.get("purchaseType") or ref_year_type.get(
                "nameRu"
            )

        supplier = values.get("Supplier")
        if isinstance(supplier, dict):
            values["supplierName"] = (
                supplier.get("supplierNameRu") or supplier.get("supplierFullNameRu") or ""
            )
            values["supplierBinIin"] = (
                supplier.get("supplierBin") or supplier.get("supplierIin") or ""
            )

        return values

    @validator("contract_period", "contract_end_date")
    def truncate_period_time(cls, v: str | None):
        if v is not None:
            return parser.parse(v).date()


class BlankGuaranteeResponse(ORJSONModel):
    contract_number: str | None = Field(None, alias="contractNumber")
    sign_date: date | None = Field(None, alias="contractSignDate")
    contract_subject: str | None = Field(None, alias="contractSubject")
    # contract_subject_kz: str | None = Field(None, alias="contractSubjectKz")
    contract_amount: str | None = Field(None, alias="contractAmount")
    guarantee_amount: str | None = Field(None, alias="guaranteeAmount")
    execution_date: date | None = Field(None, alias="executionDate")
    customer_bin_iin: str | None = Field(None, alias="customerBinIin")
    customer_name: str | None = Field(None, alias="customerName")

    contract_type: str | None = Field(None, alias="contractType")
    purchase_type: str | None = Field(None, alias="purchaseType")
    contract_period: date | None = Field(None, alias="contractPeriod")
    guarantee_period: date | None = Field(None, alias="guaranteePeriod")
    guarantee_provision_date: date | None = Field(None, alias="guaranteeProvisionDate")
    contract_end_date: date | None = Field(None, alias="contractEndDate")
    supplier_name: str | None = Field(None, alias="supplierName")
    supplier_bin_iin: str | None = Field(None, alias="supplierBinIin")

    @classmethod
    def from_orm_model(cls, source: BlankGuaranteeContract):
        guarantee_period = source.contract_period
        guarantee_provision_date = source.sign_date + timedelta(days=9)
        contract_amount = str(source.contract_amount_wnds) if source.contract_amount_wnds else None
        guarantee_amount = str(source.guarantee_amount) if source.guarantee_amount else None

        return cls(
            guarantee_period=guarantee_period,
            guarantee_provision_date=guarantee_provision_date,
            contract_number=source.contract_number,
            sign_date=source.sign_date,
            contract_subject=source.contract_subject,
            contract_amount=contract_amount,
            guarantee_amount=guarantee_amount,
            execution_date=source.fakt_execution_date or source.plan_execution_date,
            customer_bin_iin=source.customer_bin_iin,
            customer_name=source.customer_name,
            contract_type=source.contract_type,
            purchase_type=source.purchase_type,
            contract_period=source.contract_period,
            contract_end_date=source.contract_end_date,
            supplier_name=source.supplier_name,
            supplier_bin_iin=source.supplier_bin_iin,
        )


class CoveredGuaranteeContract(Guarantee):
    id: int | None = Field(None, alias="id")


class CoveredGuaranteeResponse(ORJSONModel):
    contract_number: str | None = Field(None, alias="contractNumber")
    sign_date: date | None = Field(None, alias="contractSignDate")
    contract_subject: str | None = Field(None, alias="contractSubject")
    # contract_subject_kz: str | None = Field(None, alias="contractSubjectKz")
    contract_amount: str | None = Field(None, alias="contractAmount")
    guarantee_amount: str | None = Field(None, alias="guaranteeAmount")
    execution_date: date | None = Field(None, alias="executionDate")
    customer_bin_iin: str | None = Field(None, alias="customerBinIin")
    customer_name: str | None = Field(None, alias="customerName")

    @classmethod
    def from_orm_model(cls, source: CoveredGuaranteeContract):
        return cls(
            contract_number=source.contract_number,
            sign_date=source.sign_date,
            contract_subject=source.contract_subject,
            contract_amount=(str(source.contract_amount_wnds)),
            guarantee_amount=source.guarantee_amount,
            # execution_date пришлось заменить на срок действия договора. ОБ уже зашились на
            # наименование execution_date и попросили передавать не дату исполнения, а срок
            execution_date=source.ec_end_date,
            customer_bin_iin=source.customer_bin_iin,
            customer_name=source.customer_name,
        )


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
                contractExecutionPercent=source.contract_execution_percent,
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
def _(source: Contract, target, **kwargs):
    match target:
        case type() as cls if issubclass(cls, ContractResponse):
            return ContractResponse(
                contractId=source.id,
                contractNumber=source.number,
                adId=source.advert_id,
                supplierBinIin=source.supplier_bin_iin,
                supplierName=source.ru.supplier_name,
                contractAmount=source.amount,
                contractDescription=source.ru.items_name,
                contractAmountWithoutNds=source.amount_without_nds,
                contractStartDate=source.start_date,
                contractEndDate=source.end_date,
                customerBinIin=source.customer_bin_iin,
                customerName=source.ru.customer_name,
                contractStatus=source.status,
                guaranteePercent=source.contract_execution_percent,
                **kwargs,
            )
        case type():
            raise TypeError
        case _:
            raise TypeError
