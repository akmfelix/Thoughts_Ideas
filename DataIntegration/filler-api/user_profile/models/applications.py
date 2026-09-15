from datetime import datetime

from pydantic import BaseModel, Field


class ApplicationTrdBuyStatus(BaseModel):
    id: int = Field(None, alias="id")
    name_ru: str = Field(None, alias="nameRu")
    code: str = Field(None, alias="code")


class ApplicationTrdBuy(BaseModel):
    id: int = Field(None, alias="id")
    number_anno: str = Field(None, alias="numberAnno")
    name_ru: str = Field(None, alias="nameRu")
    total_sum: float = Field(None, alias="totalSum")
    count_lots: int = Field(None, alias="countLots")
    customer_name_ru: str = Field(None, alias="customerNameRu")
    customer_bin: str = Field(None, alias="customerBin")
    start_date: datetime = Field(None, alias="startDate")
    end_date: datetime = Field(None, alias="endDate")
    status: ApplicationTrdBuyStatus = Field(None, alias="status")


class ApplitcationLotItem(BaseModel):
    lot_number: str = Field(None, alias="lotNumber")
    name_ru: str = Field(None, alias="nameRu")
    count: int = Field(None, alias="count")
    amount: float = Field(None, alias="amount")


class ApplicationRefItem(BaseModel):
    id: int = Field(None, alias="id")
    name_ru: str = Field(None, alias="nameRu")
    code: str = Field(None, alias="code")


class ApplicationLot(BaseModel):
    lot: ApplitcationLotItem = Field(None, alias="lot")
    ref: ApplicationRefItem = Field(None, alias="ref")


class ApplicationItem(BaseModel):
    supplier_id: int = Field(None, alias="supplierId")
    supplier_biniin: str = Field(None, alias="supplierBinIin")
    trd_buy: ApplicationTrdBuy = Field(None, alias="TrdBuy")
    lots: list[ApplicationLot] = Field(None, alias="lots")


class GoszakupApplications(BaseModel):
    trd_app: list[ApplicationItem] = Field(None, alias="TrdApp")
