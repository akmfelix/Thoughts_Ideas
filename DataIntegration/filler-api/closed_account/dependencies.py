import re
from typing import Annotated

from fastapi import Depends, Path

from app.exceptions import ValidationError

ACCOUNT_REGEX = r"^KZ[A-Za-z0-9]{18}$"
BIN_IIN_REGEX = r"^\d{12}$"


def _account_number_validator(
    account_number: str = Path(..., alias="accountNumber")
) -> str:
    if not account_number or not account_number.strip():
        raise ValidationError("Номер счета не может быть пустым")

    if len(account_number) != 20:
        raise ValidationError("Номер счета должен содержать ровно 20 символов")

    if not re.match(ACCOUNT_REGEX, account_number):
        raise ValidationError("Номер счета должен начинаться на KZ и содержать только буквы и цифры")

    return account_number


AccountNumber = Annotated[str, Depends(_account_number_validator)]


def _bin_iin_validator(
    bin_iin: str = Path(..., alias="biniin")
) -> str:
    if not bin_iin or not bin_iin.strip():
        raise ValidationError("БИН/ИИН не может быть пустым")

    if not re.match(BIN_IIN_REGEX, bin_iin):
        raise ValidationError("БИН/ИИН должен содержать ровно 12 цифр")

    return bin_iin


BinIin = Annotated[str, Depends(_bin_iin_validator)]
