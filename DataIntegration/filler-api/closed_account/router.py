from asyncpg import Connection
from fastapi import APIRouter, Depends

from app.api.closed_account.dependencies import AccountNumber, BinIin
from app.api.closed_account.models import ClosedAccountResponse, ClosedAccountsResponse
from app.api.closed_account.repositories import ClosedAccountRepository
from app.base import FillerResponse, FillerResponsePayload
from app.dependencies import get_collector_db
from app.utils import set_timeout

router = APIRouter(prefix="/closed-account", tags=["closed_account"])

_TIMEOUT_RESPONSE = FillerResponse(
    content=FillerResponsePayload(data={}, statusCode="timeoutError", statusName="Timeout Error")
    , status_code=400
)


@router.get("/{accountNumber}", response_model=ClosedAccountResponse)
@set_timeout(milliseconds=5_000, default_response=_TIMEOUT_RESPONSE)
async def get_closed_account(
    account_number: AccountNumber,
    connection: Connection = Depends(get_collector_db),
):
    repo = ClosedAccountRepository(connection=connection)
    account = await repo.get_closed_account(account_number=account_number)
    return ClosedAccountResponse(account=account)


@router.get("/bin/{biniin}", response_model=ClosedAccountsResponse)
@set_timeout(milliseconds=5_000, default_response=_TIMEOUT_RESPONSE)
async def get_closed_account_by_bin(
    bin_iin: BinIin,
    connection: Connection = Depends(get_collector_db),
):
    repo = ClosedAccountRepository(connection=connection)
    accounts = await repo.get_closed_account_by_bin(bin_iin=bin_iin)
    return ClosedAccountsResponse(accounts=accounts)
