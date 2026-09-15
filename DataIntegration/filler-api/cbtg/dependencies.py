import functools

from app.api.cbtg.providers import CBTGGoszakupProvider, CBTGSamrukProvider, SkPharmacyProvider
from app.settings import get_settings

settings = get_settings()


@functools.cache
def get_cbtg_goszakup_provider():
    return CBTGGoszakupProvider(
        settings=settings.httpx_client,
        token=settings.goszakup_token,
    )


@functools.cache
def get_cbtg_samruk_provider():
    return CBTGSamrukProvider(
        settings=settings.httpx_client,
    )


@functools.cache
def get_cbtg_sk_pharmacy_provider():
    return SkPharmacyProvider(
        settings=settings.httpx_client,
    )
