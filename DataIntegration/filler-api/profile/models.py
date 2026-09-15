from datetime import date, datetime
from decimal import Decimal
from enum import Enum

from fastapi import Query
from pydantic import Field, validator

from app.api.profile import utils
from app.base import ORJSONModel


class ThreeMonthPeriodProfileParams(ORJSONModel):
    biniin: str = Query(..., alias="biniin", regex=r"^\d{12}$")

    @property
    def start_date(self) -> date:
        return utils.get_month_date(months_back=3)

    @property
    def end_date(self) -> date:
        return utils.get_month_date(months_back=0)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["start_date"] = self.start_date
        d["end_date"] = self.end_date
        return d


class TransactionMeta(ORJSONModel):
    amount: str = Field(..., alias="amount")
    count: int = Field(1, alias="count")


class RefundMeta(ORJSONModel):
    count: int = Field(1, alias="count")


class Turnover(ORJSONModel):
    mcc: str = Field(None, alias="mcc")
    transactions: TransactionMeta = Field(..., alias="transactions")
    refunds: RefundMeta = Field(..., alias="refunds")


class AcquiringTurnoversV2(ORJSONModel):
    turnovers: list[Turnover] = Field([], alias="turnovers")


class SixMonthPeriodProfileParams(ORJSONModel):
    biniin: str = Query(..., alias="biniin", regex=r"^\d{12}$")

    @property
    def start_date(self) -> date:
        return utils.get_month_date(months_back=6)

    @property
    def end_date(self) -> date:
        return utils.get_month_date(months_back=0)

    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d["start_date"] = self.start_date
        d["end_date"] = self.end_date
        return d


class ProfileResponse(ORJSONModel):
    biniin: str = Field(..., alias="biniin")
    items: list | dict | None = Field(None, alias="items")

    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S"),
            date: lambda v: v.strftime("%Y-%m-%d"),
        }


class MonthPeriodMixin(ORJSONModel):
    period: date = Field(..., alias="period")

    @validator("period", pre=False, always=True)
    def validate_period(cls, value: date) -> date:
        if value.day != 1:
            raise ValueError("Period date must be the first day of the month")
        return value


class DayPeriodMixin(ORJSONModel):
    day: date = Field(..., alias="day")


'''Сущности для таблиц. Если в названии модели не указано ByDay, то выборка идет за месяц 
(постфикс - ByMonth). Просто я не хотел приписывать везде ByMonth.

Ключевые слова:
БИН или ИИН - biniin
оборот - turnover
остаток (на счету) - balance
доход - income
Халык - halyk
БВУ - stb (second tier bank)
доля (процент) - share
кол-во (целое число) - count
получатели - payees
отправители - payers
тип клиента (ЮЛ/ПБОЮЛ) - client_type
полное имя (Иванов Иван Иванович) - full_name
'''


class ClientType(str, Enum):
    LE = "ЮЛ"    # Юридическое лицо - legal entity
    IE = "ПБОЮЛ" # Индивидуальный предприниматель (ИП) - individual entrepreneur


class AverageDailyBalance(MonthPeriodMixin):
    """Среднедневные остатки по текущим и сберегательным счетам у клиента"""
    current_account_balance: Decimal | None = Field(None, alias="currentAccountBalance")
    saving_account_balance: Decimal | None = Field(None, alias="savingAccountBalance")


class Payroll(MonthPeriodMixin):
    """Фонд оплаты труда (ФОТ)"""
    payroll_balance: Decimal | None = Field(None, alias="payrollBalance")


class NOITotal(MonthPeriodMixin):
    """ЧОД в динамике по периодам (месяцам)"""
    income: Decimal | None = Field(None, alias="income")


class NOIProductCode(str, Enum):
    LOANS = "loans"
    CURRENT_ACCOUNT_AND_DEPOSITS = "currentAccountAndDeposits"
    TREASURY = "treasury"  # Дилинг
    CORPORATE_CARDS = "corporateCards"
    CASH_SETTLEMENT_SERVICES = "cashSettlementServices"
    GUARANTEES_AND_LETTERS_OF_CREDIT = "guaranteesAndLettersOfCredit" 


class NOIByProductItem(ORJSONModel):
    product_code: NOIProductCode | None = Field(None, alias="productCode")
    income: Decimal | None = Field(None, alias="income")


class NOIByProducts(MonthPeriodMixin):
    """ЧОД по продуктам"""
    items: list[NOIByProductItem] | None = Field(None, alias="items")


class ActualIncomeCategory(str, Enum):
    TREASURY = "treasury"  # Дилинг
    DEPOSITS = "deposits"
    CASH_SETTLEMENT_SERVICES = "cashSettlementServices"
    ACQUIRING = "acquiring"


class ActualIncomeProductCode(str, Enum):
    TREASURY = "treasury"  # Дилинг
    DEPOSITS = "deposits"
    CASH_SERVICES = "cashServices"
    PAYMENTS_AND_TRANSFERS = "paymentsAndTransfers"
    FX_CONTROL_AND_OTHER = "fxControlAndOther"
    TARIFF_PACKAGE = "tariffPackage"
    ACQUIRING = "acquiring"


class ActualIncomeItem(ORJSONModel):
    category: ActualIncomeCategory | None = Field(None, alias="category")
    product_code: ActualIncomeProductCode | None = Field(None, alias="productCode")
    income: Decimal | None = Field(None, alias="income")


class ActualIncome(MonthPeriodMixin):
    """Фактический доход"""
    items: list[ActualIncomeItem] | None = Field(None, alias="items")


class Margin(ORJSONModel):
    year: int | None = Field(None, alias="year")
    quarter: int | None = Field(None, alias="quarter")
    margin: Decimal | None = Field(None, alias="margin")


class WalletShareTurnover(ORJSONModel):
    outgoing_via_halyk: Decimal | None = Field(None, alias="outgoingViaHalyk")
    outgoing_via_stb: Decimal | None = Field(None, alias="outgoingViaStb")
    own_funds_stb_to_halyk: Decimal | None = Field(None, alias="ownFundsStbToHalyk")
    own_funds_halyk_to_stb : Decimal | None = Field(None, alias="ownFundsHalykToStb")
    halyk_share: Decimal | None = Field(None, alias="halykShare")


class WalletShareBalance(ORJSONModel):
    incoming_payments_halyk_current_account: Decimal | None = Field(
        None, alias="incomingPaymentsHalykCurrentAccount"
    )
    halyk_average_daily_balance: Decimal | None = Field(
        None, alias="halykAverageDailyBalance"
    )
    outgoing_payments_to_stb: Decimal | None = Field(None, alias="outgoingPaymentsToStb")
    own_funds_halyk_to_stb: Decimal | None = Field(None, alias="ownFundsHalykToStb")
    halyk_share: Decimal | None = Field(None, alias="halykShare")


class AccountTurnover(MonthPeriodMixin):
    """Средние обороты счета (по факту, просто обороты счета)"""
    turnover: Decimal | None = Field(None, alias="turnover")


class TransactionCategory(str, Enum):
    CASH_SERVICES = "cashServices"
    TRANSFER_OPERATIONS = "transferOperations"
    FX_CONVERSIONS = "fxConversions"


class AverageTransactionTicketItem(ORJSONModel):
    category: TransactionCategory | None = Field(None, alias="category")
    average_ticket: Decimal | None = Field(None, alias="averageTicket")


class AverageTransactionTicket(MonthPeriodMixin):
    """Средний чек операций"""
    items: list[AverageTransactionTicketItem] | None = Field(None, alias="items")
    transactions_count: int | None = Field(None, alias="transactionsCount")


class AcquiringTurnoverByDay(DayPeriodMixin):
    turnover: Decimal | None = Field(None, alias="turnover")


class AcquiringTurnover(MonthPeriodMixin):
    """Обороты эквайринга"""
    items: list[AcquiringTurnoverByDay] | None = Field(None, alias="items")


class AverageAcquiringTicket(MonthPeriodMixin):
    """Средний чек эквайринга"""
    average_ticket: Decimal | None = Field(None, alias="averageTicket")
    transactions_count: int | None = Field(None, alias="transactionsCount")


class QRTurnover(MonthPeriodMixin):
    """Обороты через QR"""
    turnover: Decimal | None = Field(None, alias="averageTicket")
    transactions_count: int | None = Field(None, alias="transactionsCount")


class BNPLTurnover(MonthPeriodMixin):
    """Обороты через рассрочку"""
    turnover: Decimal | None = Field(None, alias="averageTicket")
    transactions_count: int | None = Field(None, alias="transactionsCount")


class CardPaymentTurnover(MonthPeriodMixin):
    """Оплата картами - Халык vs БВУ в POS клиента"""
    halyk_turnover: Decimal | None = Field(None, alias="halykTurnover")
    halyk_transactions_count: int | None = Field(None, alias="halykTransactionsCount")
    stb_turnover: Decimal | None = Field(None, alias="stbTurnover")
    stb_transactions_count: int | None = Field(None, alias="stbTransactionsCount")


class CashTransaction(MonthPeriodMixin):
    """Кассовые операции"""
    deposit_amount: Decimal | None = Field(None, alias="depositAmount")
    withdrawal_amount: Decimal | None = Field(None, alias="withdrawalAmount")


class TransfersToSTB(ORJSONModel):
    """Переводы в другие БВУ"""
    period_from: date | None = Field(None, alias="periodFrom")
    period_to: date | None = Field(None, alias="periodTo")
    counterparty_to_stb_amount: Decimal | None = Field(None, alias="counterpartyToStbAmount")
    counterparty_to_stb_growth: Decimal | None = Field(None, alias="counterpartyToStbGrowth")


class BankType(str, Enum):
    HALYK = "halyk"
    STB = "stb"


class Counterparty(ORJSONModel):
    name: str | None = Field(None, alias="name")
    biniin: str | None = Field(None, alias="biniin")
    client_type: ClientType | None = Field(None, alias="clientType")
    turnover: Decimal | None = Field(None, alias="turnover")
    transactions_count: int | None = Field(None, alias="transactionsCount")
    bank_type: BankType | None = Field(None, alias="bankType")


class CounterpartiesTop(ORJSONModel):
    """Топ контрагентов"""
    period_from: date | None = Field(None, alias="periodFrom")
    period_to: date | None = Field(None, alias="periodTo")
    payers: list[Counterparty] | None = Field(None, alias="payers")
    payees: list[Counterparty] | None = Field(None, alias="payees")


class OwnFundsPayee(ORJSONModel):
    name: str | None = Field(None, alias="name")
    turnover: Decimal | None = Field(None, alias="turnover")
    transactions_count: int | None = Field(None, alias="transactionsCount")
    outgoing_funds_share: Decimal | None = Field(None, alias="outgoingFundsShare")


class OwnFundsPayeesTop(MonthPeriodMixin):
    """Банки-получатели собственных средств"""
    payees: list[OwnFundsPayee] | None = Field(None, alias="payees")


class SCFSupply(ORJSONModel):
    biniin: str | None = Field(None, alias="biniin")
    amount: Decimal | None = Field(None, alias="amount")
    rating: str | None = Field(None, alias="rating")
    is_client: bool | None = Field(None, alias="signClient")
    is_loan: bool | None = Field(None, alias="signLoan")
    client_name: str | None = Field(None, alias="clientName")
    client_type: str | None = Field(None, alias="clientType")


class SupplyChainFinance(ORJSONModel):
    """ФЦП"""
    counterparties_count: int | None = Field(None, alias="counterpartiesCount")
    counterparties_top: list[SCFSupply] | None = Field(None, alias="counterpartiesTop")
    anchors_count: int | None = Field(None, alias="anchorsCount")
    anchors_top: list[SCFSupply] | None = Field(None, alias="anchorsTop")


class CreditApplicationStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


class CreditApplicationAndGuarantee(ORJSONModel):
    """Кредитная заявка или гарантия"""
    product_name: str | None = Field(None, alias="productName")
    amount: Decimal | None = Field(None, alias="amount")
    date: datetime | None = Field(None, alias="date")
    status: CreditApplicationStatus | None = Field(None, alias="status")


class Signatory(ORJSONModel):
    """Подписант"""
    name: str | None = Field(None, alias="name")
    birth_date: date | None = Field(None, alias="birthDate")
    position: str | None = Field(None, alias="position")
    signature_level: int | None = Field(None, alias="signatureLevel")
    is_client: bool | None = Field(None, alias="isClient")


class BeneficialOwner(ORJSONModel):
    """Бенефициарный собственник"""
    name: str | None = Field(None, alias="name")
    client_type: ClientType | None = Field(None, alias="clientType")
    ownership_share: Decimal | None = Field(None, alias="ownershipShare")
    is_client: bool | None = Field(None, alias="isClient")


class Founder(ORJSONModel):
    """Учредитель"""
    name: str | None = Field(None, alias="name")
    client_type: ClientType | None = Field(None, alias="clientType")
    ownership_share: Decimal | None = Field(None, alias="ownershipShare")
    is_client: bool | None = Field(None, alias="isClient")


class Items(ORJSONModel):
    items: list = Field(None, alias="items")
