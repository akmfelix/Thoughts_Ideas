import asyncio
import logging

import aiohttp
from pydantic import ValidationError

from app.api.factoring.exceptions import (
    ContractNotFound,
    FactoringNotFound,
    FoundMoreThanOneContract,
)
from app.api.factoring.models import SamrukContract, SamrukFactoring
from app.exceptions import ExternalModelConversationError, ExternalServiceUnavailable
from app.providers import SamrukAioHTTPProvider
from app.settings import HttpxClientSettings

logger = logging.getLogger()


class FactoringSamrukProvider:
    contract_url = "https://integr.skc.kz/data/second-tier-bank/searchcontract?contract_number={}"
    factoring_url = "https://integr.skc.kz/data/second-tier-bank/factoring?contract_number={}"

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

    async def get_contract(self, contract_number: str):
        response = asyncio.create_task(
            self._retrieve_response(url=self.contract_url.format(contract_number))
        )

        await response
        contracts = response.result()

        if not contracts or not contracts.get("content") or not contracts["content"]:
            raise ContractNotFound
        contracts = contracts["content"]
        if len(contracts) > 1:
            raise FoundMoreThanOneContract

        contract = contracts[0]

        try:
            result = SamrukContract(**contract)
        except ValidationError as e:
            logger.exception(msg=e)
            raise ExternalModelConversationError
        return result

    async def get_factoring(self, contract_number: str) -> list[SamrukFactoring]:
        response = asyncio.create_task(
            self._retrieve_response(url=self.factoring_url.format(contract_number))
        )

        await response
        factorings = response.result()

        if not factorings or not factorings.get("content") or not factorings["content"]:
            raise FactoringNotFound
        factorings = factorings["content"]

        try:
            result = [SamrukFactoring(**factoring) for factoring in factorings]
        except ValidationError as e:
            logger.exception(msg=e)
            raise ExternalModelConversationError
        return result
