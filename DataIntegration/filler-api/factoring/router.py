import logging

from fastapi import APIRouter, Depends, Query
from fastapi.params import Security

from app.api.factoring.models import Contract, ContractResponse, SamrukContract, SamrukFactoring, Factoring, \
    FactoringResponse, FactoringResponseItem
from app.api.factoring.providers import FactoringSamrukProvider
from app.dependencies import get_factoring_samruk_provider, verify_token
from app.models import apply_conversion

logger = logging.getLogger()
router = APIRouter(prefix="/factoring", tags=["factoring"])


@router.get(
    "/samruk/contracts",
    response_model=ContractResponse,
    response_model_by_alias=True,
    dependencies=[Security(verify_token, scopes=["SAMRUK_CONTRACT:read"])]
)
async def get_samruk_contract(
    contract_number: str = Query(..., alias="contractNumber"),
    provider: FactoringSamrukProvider = Depends(get_factoring_samruk_provider),
):
    external_contract: SamrukContract = await provider.get_contract(contract_number=contract_number)
    contract: Contract = apply_conversion(external_contract, Contract)

    return apply_conversion(contract, ContractResponse)


@router.get(
    "/samruk/factoring",
    response_model=FactoringResponse,
    response_model_by_alias=True,
    dependencies=[Security(verify_token, scopes=["SAMRUK_FACTORING:read"])]
)
async def get_samruk_factoring(
    contract_number: str = Query(..., alias="contractNumber"),
    provider: FactoringSamrukProvider = Depends(get_factoring_samruk_provider),
):
    external_factorings: list[SamrukFactoring] = await provider.get_factoring(contract_number=contract_number)

    factorings: list[Factoring] = [
        apply_conversion(external_factoring, Factoring) for external_factoring in external_factorings
    ]

    return FactoringResponse(items=[apply_conversion(factoring, FactoringResponseItem) for factoring in factorings])
