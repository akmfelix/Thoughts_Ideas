from asyncpg import Connection
from fastapi import APIRouter, Depends

from app.api.reference_ul import service
from app.api.reference_ul.dependencies import AccountNumber, DateFrom, DateTo
from app.api.reference_ul.models import Reference
from app.api.reference_ul.repositories import TurnoverRepository
from app.base import FillerResponse, FillerResponsePayload
from app.dependencies import get_legal_entity_reports_db
from app.utils import set_timeout

router = APIRouter(prefix="/reference/accounts", tags=["turnover"])

_TIMEOUT_RESPONSE = FillerResponse(
    content=FillerResponsePayload(data={}, statusCode="timeoutError", statusName="Timeout Error")
    , status_code=400
)


@router.get("/{accountNumber}/turnover/daily", response_model=Reference)
@set_timeout(milliseconds=5_000, default_response=_TIMEOUT_RESPONSE)
async def get_daily(
    account_number: AccountNumber,
    _from: DateFrom,
    _to: DateTo,
    connection: Connection = Depends(get_legal_entity_reports_db),
):
    repo = TurnoverRepository(connection=connection)
    return await service.get_daily_report(repo=repo, account_number=account_number, _from=_from, _to=_to)


@router.get("/{accountNumber}/turnover/monthly", response_model=Reference)
@set_timeout(milliseconds=5_000, default_response=_TIMEOUT_RESPONSE)
async def get_monthly(
    account_number: AccountNumber,
    _from: DateFrom,
    _to: DateTo,
    connection: Connection = Depends(get_legal_entity_reports_db),
):
    repo = TurnoverRepository(connection=connection)
    return await service.get_monthly_report(repo=repo, account_number=account_number, _from=_from, _to=_to)
