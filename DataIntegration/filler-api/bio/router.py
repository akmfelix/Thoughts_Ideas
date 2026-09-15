import datetime
from decimal import Decimal

import pytz
from fastapi import APIRouter, Depends, Path, Query
from fastapi.params import Security

import app.api.bio.placeholder_data as placeholder_data
from app.api.bio import service, utils
from app.api.bio.dependencies import get_bio_provider, get_goszakup_provider
from app.api.bio.exceptions import (
    ContractNotSupportBio,
    FoundMoreThanOneContract,
    MissingContractInfoException,
    ContractNotFoundException,
    ContractStatusNotAllowed,
    ContractTypeNotAllowed,
    ContractEndDateNotAllowed, ContractEnded,
)
from app.api.bio.models import (
    BioContractResponse,
    Contract,
    ContractEnforcement,
    ContractResponse,
    ReceivedPayment,
    ReceivedPayments,
    SamrukContract
)
from app.api.bio.providers import (
    BioProvider,
    MiscGoszakupProvider,
    SamrukBioContractProvider
)
from app.base import FillerResponse
from app.dependencies import (
    Connection,
    get_bio_samruk_bio_contract_provider,
    get_guarantee_db,
    verify_token
)
from app.models import apply_conversion
from app.settings import get_settings

router = APIRouter(prefix="/bio", tags=["bio"])

settings = get_settings()


@router.get(
    "/contracts/enforcements",
    response_model=ContractEnforcement,
    response_model_by_alias=True,
)
async def get_contract_procurement(
    contract_number: str | None = Query(default=None, alias="contractNumber", min_length=1),
    contract_id: str | None = Query(default=None, alias="contractId", min_length=1),
    provider: BioProvider = Depends(get_bio_provider),
    connection: Connection = Depends(get_guarantee_db),
):
    if contract_id is None and contract_number is None:
        raise MissingContractInfoException

    contracts = await service.get_details_by_id_or_number(
        contract_number=contract_number,
        contract_id=contract_id,
        conn=connection,
    )

    if len(contracts) > 1:
        raise FoundMoreThanOneContract

    contracts = []
    if not contracts:
        if contract_id is None:
            contract_id = await provider.get_contract_id(
                contract_number=contract_number,
            )
        contract_details = await provider.parse_contract(
            contract_id=contract_id,
        )
    else:
        contract_details = contracts[0]

    return contract_details


@router.get(
    "/treasury-payments/{biniin}",
    response_model_by_alias=True,
)
async def get_treasury_payments_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    provider: MiscGoszakupProvider = Depends(get_goszakup_provider),
):
    if settings.API_MODE == "TEST" and biniin in {
        "980340000042",
        "161240013578",
        "961240000711",
        "140140020283",
    }:
        return FillerResponse(content=placeholder_data.treasury_payments.get(biniin, {}))

    current_zone = pytz.timezone("Asia/Almaty")
    current_month = datetime.datetime.now(current_zone).replace(
        tzinfo=None,
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    since_month = current_month.replace(year=current_month.year - 2)

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


@router.get(
    "/contracts/{biniin}",
)
async def get_contracts_by_bin(
    biniin: str = Path(default=..., alias="biniin"),
    next_id: int = Query(default=0, alias="nextId"),
    limit: int = Query(default=5),
    provider: MiscGoszakupProvider = Depends(get_goszakup_provider),
) -> BioContractResponse:
    result_set = await provider.get_suppliers_contracts(
        supplier_bin=biniin,
        after=next_id,
        limit=limit,
    )

    data = result_set.get("data")
    fetched_last_contract_id = result_set.get("extensions").get("pageInfo").get("lastId")
    contracts = data.get("Contract") if data.get("Contract") else []

    return BioContractResponse(
        contracts=contracts, current_id=next_id, next_id=fetched_last_contract_id
    )


@router.get(
    "/samruk/contracts",
    response_model=ContractResponse,
    response_model_by_alias=True,
    dependencies=[Security(verify_token, scopes=["BIO_SAMRUK_CONTRACT:read"])]
)
async def get_samruk_contract(
    contract_number: str = Query(..., alias="contractNumber"),
    provider: SamrukBioContractProvider = Depends(get_bio_samruk_bio_contract_provider),
):
    external_contracts: list[SamrukContract] = await provider.get_contract(contract_number=contract_number)

    # Если мы не нашли ни одного SIGNED договора
    if all(map(lambda contract: contract.status != "SIGNED", external_contracts)):
        raise ContractStatusNotAllowed

    # Порядок важен: мы сначала оставляем только SIGNED договоры и только потом вызываем ошибку если договоров оказалось
    # больше одного или ни одного
    external_contracts = list(filter(lambda contract: contract.status == "SIGNED", external_contracts))

    if not external_contracts:
        raise ContractNotFoundException
    if len(external_contracts) > 1:
        raise FoundMoreThanOneContract

    external_contract: SamrukContract = external_contracts[0]
    contract: Contract = apply_conversion(external_contract, Contract)

    if contract.contract_execution_percent is None:
        raise ContractNotSupportBio

    # "971603/2024/1" – ОК, "971603/2024/1-2" - Не ОК. С тире - это доп. соглашение, а не основной договор
    if contract.number.split("/")[-1].count("-") > 0:
        raise ContractTypeNotAllowed
    contract_type = 1  # Для ОБ цифра 1 означает основной договор

    current_date = datetime.datetime.now(pytz.utc).astimezone(pytz.timezone("Asia/Almaty"))
    if contract.end_date.year > current_date.year:
        raise ContractEndDateNotAllowed
    if contract.end_date < current_date:
        raise ContractEnded
    contract_type_year = 1  # Для ОБ цифра 1 означает, что контракт в рамках одного/этого года

    guarantee_amount = Decimal(contract.amount) * Decimal(contract.contract_execution_percent) / 100
    return apply_conversion(
        contract,
        ContractResponse,
        guarantee_amount=guarantee_amount,
        contract_type=contract_type,
        contract_type_year=contract_type_year,
    )
