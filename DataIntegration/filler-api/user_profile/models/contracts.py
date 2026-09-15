from datetime import datetime

from pydantic import BaseModel, Field


class ContractRefStatus(BaseModel):
    name_ru: str = Field(None, alias="nameRu")
    code: str = Field(None, alias="code")


class ContractCustomer(BaseModel):
    bin: str = Field(None, alias="bin")
    iin: str = Field(None, alias="iin")
    customer: int = Field(None, alias="customer")
    name: str = Field(None, alias="name")
    name_ru: str = Field(None, alias="nameRu")


class ContractTrdBuyType(BaseModel):
    id: int = Field(None, alias="id")
    name_ru: str = Field(None, alias="nameRu")
    name_kz: str = Field(None, alias="nameKz")


class ContractType(BaseModel):
    id: int = Field(None, alias="id")
    name_ru: str = Field(None, alias="nameRu")
    name_kz: str = Field(None, alias="nameKz")


class ContractTreasuryPay(BaseModel):
    pay_amount: int = Field(None, alias="payAmount")


class ContractItem(BaseModel):
    supplier_biin: str = Field(None, alias="supplierBiin")
    id: int = Field(None, alias="id")
    contract_number: str = Field(None, alias="contractNumber")
    contract_sum: str = Field(None, alias="contractSum")
    contract_sum_wnds: str = Field(None, alias="contractSumWnds")
    fakt_sum: str = Field(None, alias="faktSum")
    fakt_sum_wnds: str = Field(None, alias="faktSumWnds")
    trd_buy_number_anno: str = Field(None, alias="trdBuyNumberAnno")
    trd_buy_name_ru: str = Field(None, alias="trdBuyNameRu")
    crdate: datetime = Field(None, alias="crdate")
    sign_date: datetime = Field(None, alias="signDate")
    contract_end_date: datetime = Field(None, alias="contractEndDate")
    ec_end_date: datetime = Field(None, alias="ecEndDate")
    description_ru: str = Field(None, alias="descriptionRu")
    fin_year: int = Field(None, alias="finYear")
    contract_ms: str = Field(None, alias="contractMs")
    ref_contract_status: ContractRefStatus = Field(None, alias="RefContractStatus")
    customer: ContractCustomer = Field(None, alias="customer")
    trd_buy: dict[str, ContractTrdBuyType] = Field(None, alias="trdBuy")
    contract_type: ContractType = Field(None, alias="contractType")
    treasuery_pay: list[ContractTreasuryPay] = Field(None, alias="TreasuryPay")


class GoszakupContract(BaseModel):
    contract: list[ContractItem] = Field(None, alias="Contract")
