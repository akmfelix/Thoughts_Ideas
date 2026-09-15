from functools import cache

from fastapi import Query

from app.api.bio.covered_guarantee_utils import (
    GUARANTEE_PATTERNS,
    GuaranteeType
)
from app.api.bio.providers import (
    BioProvider,
    MiscGoszakupProvider,
    SamrukBioContractProvider
)
from app.base import FillerResponse, FillerResponsePayload
from app.exceptions import FillerHTTPException
from app.providers import HTTPProvider
from app.settings import get_settings

settings = get_settings()

GUARANTEE_NOT_FOUND_DETAIL = (
    "Сумма гарантии отсутствует в договоре. Просим обратиться в контакт центр по номеру 9595."
)


@cache
def get_samruk_bio_contract_provider():
    return SamrukBioContractProvider(
        settings=settings.httpx_client,
    )


@cache
def get_bio_provider():
    provider = BioProvider(
        settings=settings.httpx_client,
        token=settings.goszakup_token,
    )
    return provider


@cache
def get_goszakup_provider():
    return MiscGoszakupProvider(
        settings=settings.httpx_client,
        token=settings.goszakup_token,
    )


@cache
def get_http_provider():
    return HTTPProvider(settings=settings.httpx_client)


def get_guarantee_pattern(
    guarantee_type: GuaranteeType = Query(default=..., alias="guaranteeType"),
):
    guarantee_pattern = GUARANTEE_PATTERNS.get(guarantee_type)

    if guarantee_pattern is None:
        raise FillerHTTPException(detail="Guarantee type was not provided.")

    return guarantee_pattern


def guarantee_not_found_response() -> FillerResponse:
    content = FillerResponsePayload(
        data={"detail": GUARANTEE_NOT_FOUND_DETAIL},
        statusCode="guaranteeNotFound",
        statusName="Guarantee not found",
    )
    return FillerResponse(content=content, status_code=200)
