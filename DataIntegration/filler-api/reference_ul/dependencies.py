import re
from datetime import date
from typing import Annotated

from fastapi import Depends, Path, Query

from app.exceptions import ValidationError

ACCOUNT_REGEX = r"^KZ[A-Za-z0-9]{18}$"
_MIN_DATE = date(2019, 1, 1)


def get_max_allowed_date() -> date:
    today = date.today()
    if today.month == 12:
        return date(today.year + 1, 1, 1)
    return date(today.year, today.month + 1, 1)


def _date_from_validator(
    date_from: str = Query(..., alias="from")
) -> date:
    try:
        parsed_date = date.fromisoformat(date_from)
    except (ValueError, TypeError):
        raise ValidationError("Неверный формат даты `from`. Ожидается YYYY-MM-DD.")

    if parsed_date < _MIN_DATE:
        raise ValidationError("`from` out of range")

    return parsed_date


def _date_to_validator(
    date_to: str = Query(..., alias="to")
) -> date:
    try:
        parsed_date = date.fromisoformat(date_to)
    except (ValueError, TypeError):
        raise ValidationError("Неверный формат даты `to`. Ожидается YYYY-MM-DD.")

    max_limit = get_max_allowed_date()
    if parsed_date > max_limit:
        raise ValidationError("`to` out of range")

    return parsed_date


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
DateFrom = Annotated[date, Depends(_date_from_validator)]
DateTo = Annotated[date, Depends(_date_to_validator)]
