import functools

from app.api.factoring.providers import FactoringSamrukProvider
from app.settings import get_settings

settings = get_settings()


@functools.cache
def get_factoring_samruk_provider():
    return FactoringSamrukProvider(
        settings=settings.httpx_client,
    )
