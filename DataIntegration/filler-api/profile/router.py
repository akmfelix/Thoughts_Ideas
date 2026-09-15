import logging

import asyncpg
from fastapi import APIRouter, Depends, Query
from fastapi.params import Security

from app.api.profile.models import ProfileResponse, SixMonthPeriodProfileParams, AcquiringTurnoversV2
from app.api.profile.repositories import HermesRepository
from app.dependencies import verify_token, get_hermes_db
import app.api.profile.mock as mocks

logger = logging.getLogger()
router = APIRouter(prefix="/profile", tags=["profile"])



@router.get(
    "/ul/v2/acquiring-turnover",
)
async def get_acquiring_turnover_v2(
    biniin: str = Query(..., alias="biniin", regex=r"^\d{12}$"),
):
    graph = {
        "940140000385": mocks.turnovers_mock_1,
        "090140000089": mocks.turnovers_mock_2
    }

    return AcquiringTurnoversV2(turnovers=graph.get(biniin, []))


@router.get(
    "/profitability/average-balance",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_average_daily_balance(
    params: SixMonthPeriodProfileParams = Depends(),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_average_daily_balance(**params.dict())
    return ProfileResponse(biniin=params.biniin, items=customer_info)


@router.get(
    "/profitability/payroll",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_company_wage_fund(
    biniin: str = Query(..., alias="biniin", regex=r"^\d{12}$"),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_company_wage_fund(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/profitability/noi-total",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_noi_total(
    biniin: str = Query(..., alias="biniin", regex=r"^\d{12}$"),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_noi_total(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/profitability/noi-by-products",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_noi_by_products(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_noi_by_products(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/profitability/actual-income",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_actual_income(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_actual_income(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/profitability/margin",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_margin(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_margin(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/account-turnover",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_account_turnover(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_account_turnover(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/average-transaction-ticket",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_average_transaction_ticket(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_average_transaction_ticket(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/acquiring-turnover",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_acquiring_turnover(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_acquiring_turnover(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/average-acquiring-ticket",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_average_acquiring_ticket(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_average_acquiring_ticket(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/qr-turnover",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_qr_turnover(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_qr_turnover(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/bnpl-turnover",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_bnpl_turnover(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_bnpl_turnover(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/card-payment-turnover",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_card_payment_turnover(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_card_payment_turnover(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/operations/cash-transaction",
    dependencies=[Security(verify_token, scopes=["OPERATIONS_AND_POS:read"])]
)
async def get_cash_transaction(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_cash_transaction(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/counterparties/transfers-to-stb",
    dependencies=[Security(verify_token, scopes=["COUNTERPARTY_AND_FLOWS:read"])]
)
async def get_transfers_to_stb(
    biniin: str | None = Query(..., alias="biniin", regex=r"^\d{12}$"),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_transfers_to_stb(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/counterparties/supply-chain-finance",
    dependencies=[Security(verify_token, scopes=["COUNTERPARTY_AND_FLOWS:read"])]
)
async def get_supply_chain_finance(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_supply_chain_finance(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/counterparties/counterparties-top",
    dependencies=[Security(verify_token, scopes=["COUNTERPARTY_AND_FLOWS:read"])]
)
async def get_counterparties_top(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_counterparties_top(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/counterparties/own-funds-payees-top",
    dependencies=[Security(verify_token, scopes=["COUNTERPARTY_AND_FLOWS:read"])]
)
async def get_own_funds_payees_top(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_own_funds_payees_top(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/action-log/credit-applications-and-guarantees",
    dependencies=[Security(verify_token, scopes=["CRM_GOVERNANCE:read"])]
)
async def get_credit_application_and_guarantee(
    biniin: str = Query(..., alias="biniin", regex=r"^\d{12}$"),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_credit_application_and_guarantee(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/key-persons/signatories",
    dependencies=[Security(verify_token, scopes=["IDENTITY_AND_CORE_PROFILE:read"])]
)
async def get_signatories(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_signatories(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/key-persons/beneficial-owners",
    dependencies=[Security(verify_token, scopes=["IDENTITY_AND_CORE_PROFILE:read"])]
)
async def get_beneficial_owners(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_beneficial_owners(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/key-persons/founders",
    dependencies=[Security(verify_token, scopes=["IDENTITY_AND_CORE_PROFILE:read"])]
)
async def get_founders(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_founders(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/profitability/wallet-share-turnover",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_wallet_share_turnover(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_wallet_share_turnover(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)


@router.get(
    "/profitability/wallet-share-balance",
    dependencies=[Security(verify_token, scopes=["FINANCIAL_DYNAMICS:read"])]
)
async def get_wallet_share_balance(
    biniin: str | None = Query(..., alias="biniin", min_length=1),
    conn: asyncpg.Connection = Depends(get_hermes_db),
):
    repo = HermesRepository(conn)
    customer_info = await repo.get_wallet_share_balance(biniin)
    return ProfileResponse(biniin=biniin, items=customer_info)
