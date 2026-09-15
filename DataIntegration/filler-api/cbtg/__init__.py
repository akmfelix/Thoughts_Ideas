from .dependencies import (
    get_cbtg_goszakup_provider,
    get_cbtg_samruk_provider,
    get_cbtg_sk_pharmacy_provider
)
from .router import router

__all__ = (
    "get_cbtg_goszakup_provider",
    "get_cbtg_samruk_provider",
    "get_cbtg_sk_pharmacy_provider",
    "router",
)
