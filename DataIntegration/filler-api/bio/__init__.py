from .dependencies import get_samruk_bio_contract_provider
from .router import router

__all__: tuple[str, ...] = (
    'router',
    'get_samruk_bio_contract_provider'
)
