from app.api.user_profile.providers import ClientsHistoryGoszakupProvider
from app.settings import get_settings

settings = get_settings()


def get_goszakup_provider() -> ClientsHistoryGoszakupProvider:
    return ClientsHistoryGoszakupProvider(
        settings=settings.httpx_client,
        token=settings.goszakup_token,
    )
