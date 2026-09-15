from fastapi import APIRouter, Depends, Path, Query

from app.api.user_profile.dependencies import get_goszakup_provider
from app.api.user_profile.models import UserProfilesResponse
from app.api.user_profile.providers import ClientsHistoryGoszakupProvider

router = APIRouter(prefix="/user-profile/clients-history", tags=["user-profile"])


@router.get(
    "/acts/{biniin}",
)
async def get_acts_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    page: int = Query(default=0),
    limit: int = Query(default=50),
    provider: ClientsHistoryGoszakupProvider = Depends(get_goszakup_provider),
) -> UserProfilesResponse | None:
    pid = await provider.get_id_from_biniin(supplier_bin=biniin)
    if pid:
        acts = await provider.get_suppliers_acts(
            supplier_id=pid, after=page, limit=limit,
        )

        return acts
    else:
        return None


@router.get(
    "/treasury-payments/{biniin}",
)
async def get_payments_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    page: int = Query(default=0),
    limit: int = Query(default=50),
    provider: ClientsHistoryGoszakupProvider = Depends(get_goszakup_provider),
) -> UserProfilesResponse:
    payments = await provider.get_suppliers_treasury_payments(
        supplier_bin=biniin,
        after=page,
        limit=limit,
    )
    return payments


@router.get(
    "/applications/{biniin}",
    response_model=UserProfilesResponse,
    # response_model_by_alias=True,
)
async def get_applications_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    page: int = Query(default=0),
    limit: int = Query(default=50),
    provider: ClientsHistoryGoszakupProvider = Depends(get_goszakup_provider),
) -> UserProfilesResponse:
    applications = await provider.get_suppliers_applications(
        supplier_bin=biniin, after=page, limit=limit,
    )
    return applications


@router.get(
    "/contracts/{biniin}",
)
async def get_contracts_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    page: int = Query(default=0),
    limit: int = Query(default=50),
    provider: ClientsHistoryGoszakupProvider = Depends(get_goszakup_provider),
) -> UserProfilesResponse:
    return await provider.get_suppliers_contracts(
        supplier_bin=biniin, after=page, limit=limit,
    )
