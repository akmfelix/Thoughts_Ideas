import asyncio
import datetime
import re

import pytz
from fastapi import APIRouter, Depends, Path, Query
from fastapi.params import Security
from fastapi.responses import RedirectResponse

from app.api import (
    bio,
    cbtg,
    closed_account,
    factoring,
    mdm_profile,
    mvp,
    offers,
    profile,
    reference_ul,
    statgov,
    user_profile,
)
from app.api.bio import utils
from app.api.bio.covered_guarantee_utils import (
    GUARANTEE_PATTERNS,
    extract_guarantee_amount,
    resolve_guarantee_amount,
)
from app.api.bio.dependencies import (
    get_goszakup_provider,
    get_guarantee_pattern,
    get_http_provider,
    guarantee_not_found_response,
)
from app.api.bio.models import (
    BlankGuaranteeContract,
    BlankGuaranteeResponse,
    CoveredGuaranteeContract,
    CoveredGuaranteeResponse,
    ReceivedPayment,
    ReceivedPayments,
)
from app.api.bio.providers import MiscGoszakupProvider
from app.base import FillerResponse, FillerResponsePayload
from app.dependencies import (
    BinValidator,
    CustomerClaimDateValidator,
    GuaranteeRepoValidator,
    PaymentStatusValidator,
    ProductCodeValidator,
    build_optional_bearer_token_auth,
    get_directus_http_client,
    verify_token,
)
from app.exceptions import ExternalServiceUnavailable, FillerHTTPException, GuaranteeNotFound
from app.providers import DirectusHttpProvider, HTTPProvider
from app.settings import get_settings, get_starttime

settings = get_settings()
router = APIRouter(prefix="")
router.include_router(offers.router)
router.include_router(statgov.router)
router.include_router(mvp.router)
router.include_router(user_profile.router)
router.include_router(cbtg.router)
router.include_router(factoring.router)
router.include_router(bio.router)
router.include_router(mdm_profile.router)
router.include_router(profile.router)
router.include_router(
    closed_account.router,
    dependencies=[
        Depends(
            build_optional_bearer_token_auth(
                enabled=settings.closed_account_auth_enabled,
                expected_token=settings.closed_account_auth_token,
            )
        )
    ],
)
router.include_router(
    reference_ul.router,
    dependencies=[
        Depends(
            build_optional_bearer_token_auth(
                enabled=settings.reference_ul_auth_enabled,
                expected_token=settings.reference_ul_auth_token,
            )
        )
    ],
)


@router.get("/v1/statgov/{bin}", tags=["deprecated"], deprecated=True)
async def statgov_deprecated(
    bin: str = Path(..., description="БИН/ИИН компании", regex=r"^[\d]{12}$"),
):
    return RedirectResponse(url=f"/statgov/{bin}")


@router.post("/add-guarantee")
async def add_guarantee(
    biniin: BinValidator,
    payment_status: PaymentStatusValidator,
    guarantee_repo: GuaranteeRepoValidator,
    customer_claim_date: CustomerClaimDateValidator,
    product_code: ProductCodeValidator,
    guarantee_number: str = Query(default=None, alias="guaranteeNumber"),
):
    guarantee = {
        "guaranteeNumber": guarantee_number,
        "supplierBin": biniin,
        "paymentStatus": payment_status,
        "customerClaimDate": customer_claim_date,
        "productCode": product_code,
    }

    await guarantee_repo.create_guarantee(**guarantee)

    return guarantee


@router.get(
    "/supplier-guarantees",
)
async def get_guarantees_by_bin(biniin: BinValidator, guarantee_repo: GuaranteeRepoValidator):
    guarantees = await guarantee_repo.get_guarantees_by_bin(supplier_bin=biniin)
    if guarantees == [] or None:
        raise GuaranteeNotFound
    return {"content": guarantees, "meta": {"currentPage": 1, "nextPage": None}}


@router.get(
    "/ck-ip/goszakup/treasury-payments/{biniin}",
    response_model_by_alias=True,
)
async def get_treasury_payments_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    provider: MiscGoszakupProvider = Depends(get_goszakup_provider),
):
    current_zone = pytz.timezone("Asia/Almaty")
    current_month = datetime.datetime.now(current_zone).replace(
        tzinfo=None,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    since_month = current_month.replace(year=current_month.year - 1)

    received_payments: list[ReceivedPayment] = []
    async for treasury_payments in provider.get_supplier_treasury_payments(supplier_bin=biniin):
        if not treasury_payments:
            break

        # Непонятно, как провести сортировку по `pay_date` на уровне госзакупа через GraphQL.
        # В качестве временного решения мы предполагаем следующее:
        #   => если в батче нет НИ ОДНОЙ записи с датой платежа в рамках нужного интервала,
        #   => не встретим больше платежей в рамках нужного интервала дат и в последующих батчах
        if all(i.pay_date < since_month for i in treasury_payments):
            break

        received_payments += [
            ReceivedPayment(
                bik_supplier=treasury_pay.bik_supplier,
                pay_amount=treasury_pay.pay_amount,
                pay_month=treasury_pay.pay_date.strftime("%Y-%m"),
                pay_quantity=treasury_pay.pay_quantity,
            )
            for treasury_pay in treasury_payments
            if treasury_pay.pay_date > since_month
        ]

        received_payments: list[ReceivedPayment] = utils.aggregate(
            content=sorted(received_payments, key=lambda x: (x.bik_supplier, x.pay_month)),
            key_func=lambda x: (x.bik_supplier, x.pay_month),
            reduce_func=utils.reduce_received_payments,
        )

    return ReceivedPayments(bin=biniin, receivedPayments=received_payments)


@router.get("/health")
async def get_health_status():
    start_time = get_starttime()
    current_time = datetime.datetime.now(pytz.timezone("UTC")).timestamp()
    delta = current_time - start_time
    is_ready = delta >= settings.warmup_delay

    if not is_ready:
        raise FillerHTTPException(
            status_code=400,
            detail="Service is down",
            status_code_name="badRequest",
            status_name="Service is down",
        )

    content = FillerResponsePayload(
        data={"status": "up"},
        statusCode="OK",
        statusName="OK",
    )
    return FillerResponse(content=content, status_code=200)


@router.get(
    "/covered-guarantee", dependencies=[Security(verify_token, scopes=["COVERED_GUARANTEE:read"])]
)
async def get_covered_guarantee_by_contract_number(
    contract_number: str = Query(default=..., alias="contractNumber"),
    guarantee_amount_pattern: re.Pattern = Depends(get_guarantee_pattern),
    goszakup_provider: MiscGoszakupProvider = Depends(get_goszakup_provider),
    http_provider: HTTPProvider = Depends(get_http_provider),
    aio_http_provider: DirectusHttpProvider = Depends(get_directus_http_client),
):
    contract = await goszakup_provider.get_covered_guarantee_contract(
        contract_number=contract_number
    )
    covered_guarantee = CoveredGuaranteeContract(**contract)

    covered_guarantee_amount = await resolve_guarantee_amount(
        registry_number=covered_guarantee.id,
        guarantee_amount_pattern=guarantee_amount_pattern,
        http_provider=http_provider,
        aio_http_provider=aio_http_provider,
        timeout=min(settings.MIN_TIMEOUT_MS, settings.global_endpoint_timeout_ms),
        contract_file_path=covered_guarantee.contract_file_path,
    )

    if covered_guarantee_amount is not None:
        covered_guarantee.guarantee_amount = covered_guarantee_amount
        return CoveredGuaranteeResponse.from_orm_model(covered_guarantee)

    return guarantee_not_found_response()


@router.get(
    "/blank-guarantee/antidumping",
    dependencies=[Security(verify_token, scopes=["BLANK_GUARANTEE:read"])],
)
async def get_blank_guarantee_by_contract_number(
    contract_number: str = Query(default=..., alias="contractNumber"),
    goszakup_provider: MiscGoszakupProvider = Depends(get_goszakup_provider),
    http_provider: HTTPProvider = Depends(get_http_provider),
    aio_http_provider: DirectusHttpProvider = Depends(get_directus_http_client),
):
    if contract_number == "050340005347/260313/00":
        return BlankGuaranteeResponse(
            **{
            "contract_number": "050340005347/260313/00",
            "contractSignDate": "2026-09-07",
            "contractSubject": "Теплодымокамера",
            "contractAmount": "95971272.96",
            "guaranteeAmount": "16000000.03",
            "executionDate": "2026-12-06",
            "customerBinIin": "050340005347",
            "customerName": "ГУ \"Департамент по чрезвычайным ситуациям Атырауской области Министерства по чрезвычайным ситуациям Республики Казахстан\"",
            "contractType": "Основной договор",
            "purchaseType": "Однолетний",
            "contractPeriod": "2026-12-31",
            "guaranteePeriod": "2026-12-31",
            "guaranteeProvisionDate": "2026-09-16",
            "contractEndDate": None,
            "supplierName": "ТОО \"ИндастриалПартс\"",
            "supplierBinIin": "230140028466"
          }
        )

    contract = await goszakup_provider.get_blank_guarantee_contract(contract_number=contract_number)
    blank_guarantee = BlankGuaranteeContract(**contract)

    blank_guarantee_amount = await resolve_guarantee_amount(
        registry_number=blank_guarantee.id,
        guarantee_amount_pattern=GUARANTEE_PATTERNS.get("ANTIDUMPING"),
        http_provider=http_provider,
        aio_http_provider=aio_http_provider,
        timeout=min(settings.MIN_TIMEOUT_MS, settings.global_endpoint_timeout_ms),
        contract_file_path=blank_guarantee.contract_file_path,
    )

    if blank_guarantee_amount is not None:
        blank_guarantee.guarantee_amount = blank_guarantee_amount
        return BlankGuaranteeResponse.from_orm_model(blank_guarantee)

    return guarantee_not_found_response()


# TODO: это просто mock для разделения
@router.get(
    "/noncovered-guarantee",
)
async def get_noncovered_guarantee_by_contract_number(
    contract_number: str = Query(default=..., alias="contractNumber"),
    goszakup_provider: MiscGoszakupProvider = Depends(get_goszakup_provider),
    http_provider: HTTPProvider = Depends(get_http_provider),
):
    contract = await goszakup_provider.get_blank_guarantee_contract(contract_number=contract_number)
    blank_guarantee = BlankGuaranteeContract(**contract)

    contract_file_path = blank_guarantee.contract_file_path
    if contract_file_path is not None:
        response = await http_provider.get(url=contract_file_path)
        contract_file_content = response.content
        try:
            # Про тред смотри выше в функции get_obligations_guarantee_by_contract_number
            blank_guarantee_amount = await asyncio.wait_for(
                asyncio.to_thread(
                    extract_guarantee_amount,
                    contract_file_content,
                    GUARANTEE_PATTERNS.get("ANTIDUMPING"),
                ),
                timeout=min(settings.MIN_TIMEOUT_MS, settings.global_endpoint_timeout_ms),
            )
        except asyncio.TimeoutError:
            raise ExternalServiceUnavailable
        else:
            if blank_guarantee_amount is not None:
                blank_guarantee.guarantee_amount = blank_guarantee_amount
                return BlankGuaranteeResponse.from_orm_model(blank_guarantee)

            return guarantee_not_found_response()
