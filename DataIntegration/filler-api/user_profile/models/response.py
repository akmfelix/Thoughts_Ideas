from pydantic import BaseModel, validator


class UserProfilesResponse(BaseModel):
    items: list = []
    page: int = 0
    next_page: int

    @validator("items", pre=True)
    def items_validation(cls, value):
        if value is None:
            value = []

        return value
