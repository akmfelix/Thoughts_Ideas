from datetime import datetime

from pydantic import BaseModel, Field


class TreasuryPayItem(BaseModel):
    id: int = Field(None, alias="id")
    nom_za: str = Field(None, alias="nomZa")
    contract_id: int = Field(None, alias="contractId")
    dt_reg: datetime = Field(None, alias="dtReg")
    nom_uved: str = Field(None, alias="nomUved")
    supplier: str = Field(None, alias="supplier")
    rnn_Supplier: str = Field(None, alias="rnnSupplier")
    bik_Supplier: str = Field(None, alias="bikSupplier")
    iik_Supplier: str = Field(None, alias="iikSupplier")
    code_Supplier: str = Field(None, alias="codeSupplier")
    nom_dog: str = Field(None, alias="nomDog")
    dt_dog: datetime = Field(None, alias="dtDog")
    item_description: str = Field(None, alias="itemDescription")
    quantity: int = Field(None, alias="quantity")
    unit_price: float = Field(None, alias="unitPrice")
    nom_dop: str = Field(None, alias="nomDop")
    dt_dop: datetime = Field(None, alias="dtDop")
    type_bujet: str = Field(None, alias="typeBujet")
    budget_name_ru: str = Field(None, alias="budgetNameRu")
    budget_name_kz: str = Field(None, alias="budgetNameKz")
    kato: str = Field(None, alias="kato")
    func: str = Field(None, alias="func")
    espk: str = Field(None, alias="espk")
    gu: str = Field(None, alias="gu")
    fin_source: str = Field(None, alias="finSource")
    po_header_id: int = Field(None, alias="poHeaderId")
    last_update_date: datetime = Field(None, alias="lastUpdateDate")
    vendor_id: int = Field(None, alias="vendorId")
    pdi_update_date: datetime = Field(None, alias="pdiUpdateDate")
    prepay_sum: int = Field(None, alias="prepaySum")
    str_prepay_sum: str = Field(None, alias="strPrepaySum")
    check_id: int = Field(None, alias="checkId")
    invoiced: int = Field(None, alias="invoiceId")
    pay_description: str = Field(None, alias="payDescription")
    invnum: str = Field(None, alias="invnum")
    pay_amount: int = Field(None, alias="payAmount")
    check_number: str = Field(None, alias="checkNumber")
    pay_date: datetime = Field(None, alias="payDate")
    code_combination_id: int = Field(None, alias="codeCombinationId")
    ppn: int = Field(None, alias="ppn")
    accounting_date: int = Field(None, alias="accountingDate")
    index_date: datetime = Field(None, alias="indexDate")
    system_id: int = Field(None, alias="systemId")


class TreasuryPay(BaseModel):
    treasury_pay: list[TreasuryPayItem] = Field(None, alias="TreasuryPay")


class GoszakupContract(BaseModel):
    contract: list[TreasuryPay] = Field(None, alias="Contract")
