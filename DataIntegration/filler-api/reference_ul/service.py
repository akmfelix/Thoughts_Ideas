from datetime import date

from app.api.reference_ul.models import Reference
from app.api.reference_ul.repositories import TurnoverRepository
from app.exceptions import ValidationError


async def get_daily_report(
    repo: TurnoverRepository,
    account_number: str,
    _from: date,
    _to: date
) -> Reference:

    if _from > _to:
        raise ValidationError("Дата начала не может быть позже даты конца")

    reference: Reference = await repo.get_daily_turnover(date_from=_from, date_end=_to, account_number=account_number)
    return reference


async def get_monthly_report(
    repo: TurnoverRepository,
    account_number: str, 
    _from: date,
    _to: date
) -> Reference:

    if _from > _to:
        raise ValidationError("Дата начала не может быть позже даты конца")

    reference: Reference = await repo.get_monthly_turnover(date_from=_from, date_end=_to, account_number=account_number)
    return reference
