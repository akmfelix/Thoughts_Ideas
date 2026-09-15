from datetime import datetime

from pydantic import BaseModel, Field


class ActItem(BaseModel):
    id: int = Field(None, alias="id")
    akt_date: datetime = Field(None, alias="aktDate")
    number_act: str = Field(None, alias="numberAct")
    create_date_act: datetime = Field(None, alias="createDateAct")
    contract_root_id: int = Field(None, alias="contractRootId")
    status_id: int = Field(None, alias="statusId")
    is_deleted: int = Field(None, alias="isDeleted")
    day_overdue: int = Field(None, alias="dayOverdue")
    sum_avans: str = Field(None, alias="sumAvans")
    sum_beginning: str = Field(None, alias="sumBeginning")
    sum_fine: str = Field(None, alias="sumFine")
    sum_previously: str = Field(None, alias="sumPreviously")
    sum_transfer: str = Field(None, alias="sumTransfer")
    create_date_gen_info: datetime = Field(None, alias="createDateGenInfo")
    status_name_ru: str = Field(None, alias="statusNameRu")
    status_name_kz: str = Field(None, alias="statusNameKz")
    supplier_id: int = Field(None, alias="supplierId")
    customer_id: int = Field(None, alias="customerId")
    is_gu: int = Field(None, alias="isGu")
    type_act: int = Field(None, alias="typeAct")
    ref_subject_type_id: int = Field(None, alias="refSubjectTypeId")
    parent_id: int = Field(None, alias="parentId")
    system_id: int = Field(None, alias="systemId")
    index_date: datetime = Field(None, alias="indexDate")
    approve_date: datetime = Field(None, alias="approveDate")


class GoszakupActs(BaseModel):
    acts: list[ActItem] = Field(None, alias="Acts")
