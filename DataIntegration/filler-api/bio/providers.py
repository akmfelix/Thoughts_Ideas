import asyncio
import logging
import re
import typing

import aiohttp
from pydantic import ValidationError

from app.api.bio.exceptions import ContractNotFound, FoundMoreThanOneContract
from app.api.bio.models import SamrukContract, TreasuryPay
from app.exceptions import ExternalModelConversationError, ExternalServiceUnavailable
from app.providers import GoszakupProvider, HTTPProvider, SamrukAioHTTPProvider
from app.settings import HttpxClientSettings

logger = logging.getLogger()


class SamrukBioContractProvider:
    contract_url = "https://integr.skc.kz/data/second-tier-bank/searchcontract?contract_number={}"

    def __init__(self, settings: HttpxClientSettings):
        self.provider = SamrukAioHTTPProvider(settings=settings)

    async def _retrieve_response(self, url: str):
        response = await self.provider.get(url=url)
        try:
            response.raise_for_status()
        except aiohttp.ClientError as e:
            logger.exception(msg=e)
            raise ExternalServiceUnavailable(status_code=424)
        result = await response.json()
        return result

    async def get_contract(self, contract_number: str) -> list[SamrukContract]:
        response = asyncio.create_task(
            self._retrieve_response(url=self.contract_url.format(contract_number))
        )

        await response
        contracts = response.result()

        if not contracts or contracts.get("content") is None:
            raise ExternalModelConversationError  # Самрук отдал некорректный ответ

        if not contracts["content"]:
            raise ContractNotFound

        contracts = contracts["content"]
        try:
            result = [SamrukContract(**contract) for contract in contracts]
        except ValidationError as e:
            logger.exception(msg=e)
            raise ExternalModelConversationError
        return result


class BioProvider(GoszakupProvider):
    base_url = "https://goszakup.gov.kz/ru/egzcontract/cpublic/enforcements/{}"

    patterns = {
        "absenceSecurityPerformanceContract": re.compile(
            r"\s+".join("По договору отсутствуют Обеспечения исполнения договора".split())
        ),
        "securityDepositTotalAmountContract": re.compile(
            r"\s+".join("гарантийный денежный взнос на \d+% от общей суммы договора".split())
        ),
        "bankGuaranteeAmountInAccordanceLaw26": re.compile(
            r"\s+".join("банковская гарантия на сумму в соответствии со статьей 26 Закона".split())
        ),
        "cashGuaranteeAmountInAccordanceLaw26": re.compile(
            r"\s+".join(
                "гарантийный денежный взнос на сумму в соответствии со статьей 26 Закона".split()
            )
        ),
        "ewalletCollateralMoney3percentContractAmount": re.compile(
            r"\s+".join(
                "Обеспечение с денег электронного кошелька на \d+% от общей суммы договора".split()
            )
        ),
        "ewalletMoneyAmountInAccordanceLaw26": re.compile(
            r"\s+".join("Обеспечение с денег электронного кошелька на сумму в соответствии со статьей 26 Закона".split())
        ),
        "bankGuaranteeAmountInAdvanceUnderContract": re.compile(
            r"\s+".join("банковская гарантия на сумму аванса по договору".split())
        ),
        "civilLiabilityInsurance3percentTotalContractAmount": re.compile(
            r"\s+".join("Договор страхования гражданско-правовой ответственности на \d+% от общей суммы договора".split())
        ),
        "bankGuarantee3percentTotalContractAmount": re.compile(
            r"\s+".join("банковская гарантия на \d+% от общей суммы договора".split())
        ),
        "attachmentStatus": re.compile(
            r"Статус прикрепления:\r\n +<span class=\"name\">(.*)</span>"
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        settings = HttpxClientSettings(verify=False)
        self.http_provider = HTTPProvider(settings=settings)

    async def get_contract_id(
        self,
        contract_number: str,
    ):
        query_string = """
           query getContractNumberId($contractNumberSys: String!){
                Contract (filter: {contractNumberSys: $contractNumberSys}) {
                    id
                }
           }
        """

        variables = {"contractNumberSys": contract_number}
        headers = {"Authorization": f"Bearer {self.token}"}
        graphql_response = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )

        data = graphql_response.json()
        contract_list = data["data"]["Contract"]

        if contract_list is None:
            raise ContractNotFound

        if len(contract_list) > 1:
            raise FoundMoreThanOneContract

        contract_id = contract_list[0]["id"]

        return contract_id

    async def parse_contract(self, contract_id):
        http_page = await self.http_provider.get(url=self.base_url.format(contract_id))
        result = await self.extract_enforcements(text=http_page.text)
        return result

    async def extract_enforcements(self, text):
        result = {}
        for key, value in self.patterns.items():
            search_result = re.search(value, text)

            if search_result is None:
                continue
            if (
                len(search_result.groups()) > 0
            ):  # Checking 'attachmentStatus' is found or not on the goszakup webpage
                result[key] = search_result.group(1)
            else:
                result[key] = 1
        return result


class MiscGoszakupProvider(GoszakupProvider):
    async def get_supplier_treasury_payments(
        self,
        supplier_bin: str,
        treasury_pays: list[TreasuryPay] = None,
        after: int = 0,
    ) -> typing.AsyncGenerator[list[TreasuryPay], typing.Any]:
        query_string = """
           query ($supplierBin: String!, $after: Int!){
               Contract (filter: {supplierBiin: $supplierBin}, limit: 200, after: $after) {
                   treasuryPay: TreasuryPay {
                       bikSupplier,
                       supplierName: supplier,
                       payDescription,
                       payAmount,
                       payDate: payDate
                   }
               }
           }
               """
        if treasury_pays is None:
            treasury_pays: list[TreasuryPay] = []

        variables = {"supplierBin": supplier_bin, "after": after}
        headers = {"Authorization": f"Bearer {self.token}"}
        res = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )
        result = res.json()
        contracts = result.get("data").get("Contract")

        if contracts is None:
            yield []

        for contract in contracts:
            if contract.get("treasuryPay") is None:
                continue

            treasury_pays += [TreasuryPay(**data) for data in contract.get("treasuryPay")]

        yield treasury_pays

        if result.get("extensions").get("pageInfo").get("hasNextPage"):
            last_id = result.get("extensions").get("pageInfo").get("lastId")
            async for treasury_pays in self.get_supplier_treasury_payments(
                supplier_bin=supplier_bin,
                after=last_id,
            ):
                yield treasury_pays

    async def get_blank_guarantee_contract(self, contract_number: str):
        query = """
            query GetBlankGuaranteeContractDetails($contractNumber: String!) {
                Contract(
                    filter: {
                        contractNumberSys: $contractNumber
                        refContractTypeId: 1 # Тип договора (1 - основной договор)
                        refContractStatusId: 190 # Статус договора (190 - действующий)
                    }
                ) {
                    refContractYearTypeId # Тип закупки (1 - однолетний)
                    refContractAgrFormId  # форма заключения (2 - нетиповая форма, 3 - не посредством портала)
                    contractNumber: contractNumberSys
                    Customer {
                        customerBin: bin
                        customerNameRu: nameRu
                        customerFullNameRu: fullNameRu
                    }
                    RefContractType {
                        contractType: nameRu
                    }
                    RefContractYearType {
                        purchaseType: nameRu
                    }
                    File {
                        contractFilePath: filePath
                    }
                    Supplier {
                        supplierNameRu: nameRu
                        supplierFullNameRu: fullNameRu
                        supplierBin: bin
                        supplierIin: iin
                    }
                    id
                    contractSignDate: signDate # это также и дата заключения договора
                    contractSubjectRu: descriptionRu
                    contractSubjectKz: descriptionKz
                    contractPeriod: ecEndDate # это также и срок гарантии 
                    contractAmountWnds: contractSumWnds
                    planExecDate
                    faktExecDate
                    contractEndDate
                }
            }
        """
        variables = {"contractNumber": contract_number}
        headers = {"Authorization": f"Bearer {self.token}"}

        response = await self.provider.execute(
            url=self.url,
            query=query,
            variables=variables,
            headers=headers,
        )

        contract = None
        response = response.json().get("data", {})
        if isinstance(response, dict):
            contract = response.get("Contract", [])
            if contract:
                contract_data = contract[0]
                if any(
                    (
                        contract_data.get("refContractAgrFormId") in [2, 3],
                        contract_data.get("refContractYearTypeId") != 1,
                    )
                ):
                    raise ContractNotFound

        if not contract:
            raise ContractNotFound

        if len(contract) > 1:
            raise FoundMoreThanOneContract

        return contract[0]

    async def get_covered_guarantee_contract(self, contract_number: str):
        query = """
            query GetCoveredGuaranteeContractDetails($contractNumber: String!) {
                Contract(
                    filter: {
                        contractNumberSys: $contractNumber
                        refContractTypeId: 1 # Тип договора (1 - основной договор)
                        refContractStatusId: 190 # Статус договора (190 - действующий)
                    }
                ) {
                    refContractAgrFormId # форма заключения (2 - нетиповая форма, 3 - не посредством портала)
                    contractNumber: contractNumberSys
                    id
                    contractSignDate: signDate # Дата договора
                    contractSubjectRu: descriptionRu # Предмет договора на русском
                    contractSubjectKz: descriptionKz # Предмет договора на казахском
                    contractAmountWnds: contractSumWnds # Сумма договора с НДС
                    planExecDate # Срок исполнения (плановый)
                    faktExecDate # Срок исполнения (фактический)
                    ecEndDate # Срок действия
                    contractEndDate
                    
                    Customer {
                        customerBin: bin
                        customerNameRu: nameRu
                        customerFullNameRu: fullNameRu
                    }
                    
                    File {
                        contractFilePath: filePath
                    }
                }
            }
        """

        variables = {"contractNumber": contract_number}
        headers = {"Authorization": f"Bearer {self.token}"}

        response = await self.provider.execute(
            url=self.url,
            query=query,
            variables=variables,
            headers=headers,
        )

        contract = None
        response = response.json().get("data", {})

        if isinstance(response, dict):
            contract = response.get("Contract", [])
            if contract and contract[0].get("refContractAgrFormId") in [2, 3]:
                raise ContractNotFound

        if not contract:
            raise ContractNotFound

        if len(contract) > 1:
            raise FoundMoreThanOneContract

        return contract[0]

    async def get_suppliers_contracts(
        self: "MiscGoszakupProvider", supplier_bin: str, after: int, limit: int
    ) -> dict:
        """Номер договора
        Тип договора (основной договор/доп. соглашение)
        Тип закупки (Однолетний/многолетний)
        Дата заключения договора
        Номер объявления
        Наименование объявления
        БИН заказчика
        Наименование заказчика
        Сумма с ндс
        Сумма без ндс
        Способ закупки"""
        query_string = """
            query ($limit: Int!, $after: Int!, $supplierBin: String!) {
                Contract (limit: $limit, after: $after, filter: {supplierBiin: $supplierBin})
                {
                    id
                    contractNumber: contractNumberSys
                    contractType: refContractTypeId # тип договора 1 - основной договор 2 - допик
                    contractYearType: refContractYearTypeId # Тип закупки (1-Однолетний / 2-многолетний)
                    signDate  # Дата подписания

                    adNumber: trdBuyNumberAnno # Номер объявления
                    adName: trdBuyNameRu # Наименование объявления

                    # Заказчик
                    customer: Customer {
                        bin # БИН заказчика
                        iin # ИИН заказчика
                        nameRu # Наименование заказчика
                    }

                    contractSum  # Сумма заключенного контракта без ндс
                    contractSumWnds # Сумма заключенного контракта с ндс
                    faktSum  # Сумма фактических выплат без ндс
                    faktSumWnds  # Сумма фактических выплат c ндс

                    FaktTradeMethods { # способ закупки
                        nameRu
                        symbolCode
                    }

                    RefContractStatus { # Статус договора
                        nameRu
                    }
                }
            }
        """

        variables = {"supplierBin": supplier_bin, "after": after, "limit": limit}
        headers = {"Authorization": f"Bearer {self.token}"}

        result_set = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )
        return result_set.json()
