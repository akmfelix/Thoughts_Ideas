from datetime import date

import asyncpg

from app.api.reference_ul.models import Reference
from app.repositories import BaseRepositoryMetaclass


class TurnoverRepository(metaclass=BaseRepositoryMetaclass):
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def get_daily_turnover(self, date_from: date, date_end: date, account_number: str):
        result = await self.connection.fetch(
            self.query_get_account_turnover_daily,
            date_from,
            date_end,
            account_number
        )
        return Reference(**result[0]) if result else None

    async def get_monthly_turnover(self, date_from: date, date_end: date, account_number: str):
        result = await self.connection.fetch(
            self.query_get_account_turnover_monthly,
            date_from,
            date_end,
            account_number
        )
        return Reference(**result[0]) if result else None
