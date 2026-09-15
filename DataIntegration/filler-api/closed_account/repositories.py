import asyncpg

from app.api.closed_account.models import (
    ClosedAccount,
    ClosedAccountByBin,
)
from app.repositories import BaseRepositoryMetaclass


class ClosedAccountRepository(metaclass=BaseRepositoryMetaclass):
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def get_closed_account(self, account_number: str) -> ClosedAccount | None:
        result = await self.connection.fetchrow(
            self.query_get_closed_account,
            account_number
        )
        
        if not result:
            return None
        
        return ClosedAccount(**result)

    async def get_closed_account_by_bin(self, bin_iin: str) -> list[ClosedAccountByBin]:
        result = await self.connection.fetch(
            self.query_get_closed_account_by_bin,
            bin_iin
        )

        if not result:
            return []

        accounts = [ClosedAccountByBin(**row) for row in result]
        return accounts
