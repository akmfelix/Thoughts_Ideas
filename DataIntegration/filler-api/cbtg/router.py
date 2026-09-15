import datetime
import logging
import random

import pytz
from dishka.integrations.fastapi import FromDishka, inject
from fastapi import APIRouter, Depends, Path

from app.api.cbtg.exceptions import (
    AdNotFound,
    AdNotFoundException,
    FoundMoreThanOneAdException,
    GoszakupAdBuyStatusDocsChangedNotAllowed,
    GoszakupAdBuyStatusNotAllowed,
    GoszakupAdTradeMethodNotAllowed,
    HealthCheckNotPassed,
    SamrukAdBuyStatusNotAllowed,
    SamrukAdBuyStatusNotAllowedException,
    TenderEnded,
    TenderNotStarted,
)
from app.api.cbtg.models import (
    GoszakupTrdBuy,
    GoszakupTrdBuyResponse,
    HealthCheckResponse,
    SamrukAd,
    SamrukAdResponse,
    SkPharmacyAd,
    SkPharmacyAdResponse,
)
from app.api.cbtg.providers import CBTGGoszakupProvider, CBTGSamrukProvider, SkPharmacyProvider
from app.dependencies import (
    get_cbtg_sk_pharmacy_provider,
)

logger = logging.getLogger()
router = APIRouter(prefix="/cbtg", tags=["CBTG"])


@router.get(
    "/goszakup/health",
    response_model_by_alias=True,
)
@inject
async def goszakup_health_check(provider: FromDishka[CBTGGoszakupProvider]):
    try:
        ad_number = str(random.randint(10_000_000, 100_000_000)) + "-1"
        GoszakupTrdBuy(**await provider.get_ad(ad_number))
        health_passed = True

    except (AdNotFoundException, FoundMoreThanOneAdException):
        health_passed = True  # закупка может быть не найдена, главное, что Госзакуп работает

    except Exception as e:
        logger.exception(msg=e)
        health_passed = False

    if health_passed:
        return HealthCheckResponse(
            statusCode="OK",
            statusName="OK",
        )
    else:
        raise HealthCheckNotPassed


@router.get(
    "/samruk/health",
    response_model_by_alias=True,
)
@inject
async def samruk_health_check(provider: FromDishka[CBTGSamrukProvider]):
    try:
        ad_number = "777-1"
        if random.randint(1, 100) > 95:
            SamrukAd(**await provider.get_ad(ad_number))
        health_passed = True

    except (AdNotFoundException, FoundMoreThanOneAdException, SamrukAdBuyStatusNotAllowedException):
        health_passed = True  # закупка может быть не найдена, главное, что Самрук работает

    except Exception as e:
        logger.exception(msg=e)
        health_passed = False

    if health_passed:
        return HealthCheckResponse(
            statusCode="OK",
            statusName="OK",
        )
    else:
        raise HealthCheckNotPassed


@router.get(
    "/goszakup/ad/{adNumber}",
    # response_model=GoszakupTrdBuyResponse,
    response_model_by_alias=True,
)
@inject
async def get_goszakup_ad(
    provider: FromDishka[CBTGGoszakupProvider],
    ad_number: str = Path(default=..., alias="adNumber"),
):
    """

    Args:
        ad_number:
        provider:

    Допустимые для подачи на бланковую тендерную гарантию `статусы` закупок:
        PublishedPriceOffers: Опубликовано (прием ценовых предложений)
        PublishedAdditionDemands: Опубликовано (дополнение заявок)
        PublishedOrderTaking: Опубликовано (прием заявок)

    Способы закупок по которым допустим выпуск бланковой тендерной гарантии:

    """
    trd_buy: GoszakupTrdBuy = GoszakupTrdBuy(**await provider.get_ad(ad_number=ad_number))

    current_zone = pytz.timezone("Asia/Almaty")
    current_time = datetime.datetime.now(current_zone).replace(tzinfo=None)

    trd_buy.lots = list(filter(lambda lot: lot.status_code != "Cancelled", trd_buy.lots))

    if trd_buy.start_date > current_time:
        raise TenderNotStarted

    if trd_buy.end_date < current_time:
        raise TenderEnded

    if trd_buy.status_code == "DocumentationСhanged":
        raise GoszakupAdBuyStatusDocsChangedNotAllowed

    if trd_buy.status_code not in {
        "PublishedPriceOffers",
        "PublishedAdditionDemands",
        "PublishedOrderTaking",
    }:
        raise GoszakupAdBuyStatusNotAllowed

    if len(trd_buy.lots) == 0:
        raise AdNotFound

    if trd_buy.trade_method_id not in {
        2,
        3,
        7,
        8,
        22,
        32,
        50,
        52,
        60,
        77,
        78,
        120,
        121,
        122,
        124,
        126,
        128,
        129,
        130,
        132,
        133,
        160,
        177,
        188,
        200,
    }:
        raise GoszakupAdTradeMethodNotAllowed

    return GoszakupTrdBuyResponse(**trd_buy.dict())


@router.get(
    "/samruk/ad/{adNumber}",
    response_model=SamrukAdResponse,
    response_model_by_alias=True,
)
@inject
async def get_samruk_ad(
    provider: FromDishka[CBTGSamrukProvider],
    ad_number: str = Path(default=..., alias="adNumber"),
):
    ad: SamrukAd = await provider.get_ad(ad_number=ad_number)

    current_zone = pytz.timezone("Asia/Almaty")
    current_time = datetime.datetime.now(current_zone)
    print(current_time, ad.start_date, ad.end_date)

    if ad.start_date > current_time:
        raise TenderNotStarted

    if ad.end_date < current_time:
        raise TenderEnded

    if ad.status_code not in {"PUBLISHED"}:
        raise SamrukAdBuyStatusNotAllowed

    return ad.dict()


@router.get(
    "/sk-pharmacy/ad/{adNumber}",
    response_model=SkPharmacyAdResponse,
    response_model_by_alias=True,
)
async def get_sk_pharmacy_ad(
    ad_number: str = Path(default=..., alias="adNumber"),
    provider: SkPharmacyProvider = Depends(get_cbtg_sk_pharmacy_provider),
):
    ad: SkPharmacyAd = await provider.get_ad(ad_number=ad_number)

    current_zone = pytz.timezone("Asia/Almaty")
    current_time = datetime.datetime.now(current_zone).replace(tzinfo=None)

    if ad.start_date > current_time:
        raise TenderNotStarted

    if ad.end_date < current_time:
        raise TenderEnded

    return ad.dict()
