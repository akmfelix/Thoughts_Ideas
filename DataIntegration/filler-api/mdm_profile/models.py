from pydantic import Field

from app.base import ORJSONModel


class AcquiringTurnover(ORJSONModel):
    biniin: str = Field(..., alias="biniin")
    sum_w4_last2_month: str | None = Field(None, alias="sumW4TransLast2Month")


class HalykEmployee(ORJSONModel):
    ocrm_id: str | None = Field(None, alias="ocrmId")
    public_id: str | None = Field(None, alias="publicId")
    employee_code: str | None = Field(None, alias="employeeCode")
    trusted_phone_number: str | None = Field(None, alias="trustedPhoneNumber", exclude=True)
    is_employee: bool | None = Field(None, alias="isEmployee")
    email: str | None = Field(None, alias="email")

