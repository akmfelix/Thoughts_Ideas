import asyncpg
from fastapi.concurrency import run_in_threadpool
from app.api.mdm_profile.exceptions import UserNotFound
from app.repositories import BaseRepositoryMetaclass
from app.settings import get_settings

settings = get_settings()

# Дефолтные лимиты (можно вынести в конфиг или БД)
DEFAULT_LIMITS = {
    "min_turnover": 100000.0,
    "avg_ticket_min": 500.0,
    "avg_ticket_max": 500000.0,
    "max_returns_ratio": 5.0
}


class MDMrepository(metaclass=BaseRepositoryMetaclass):
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def get_acquiring_turnover_by_biniin(self, biniin: str):
        query = self.query_get_acquiring_turnover_by_biniin
        params = {"biniin": biniin}
        result = await run_in_threadpool(self.execution_query_to_db, query, params)
        return result


    async def get_employee_by_ocrm_public_id(self, ocrm_id: str | None, public_id: str | None):
        public_id = public_id if public_id is None else public_id.upper()
        ocrm_id = ocrm_id if ocrm_id is None else ocrm_id.upper()
        params = {"public_id": public_id, "ocrm_id": ocrm_id}
        query = self.query_get_employee_by_ocrm_public_id
        result = await run_in_threadpool(self.execution_query_to_db, query, params)
        if not result:
            raise UserNotFound
        return result

    def execution_query_to_db(self, query, params):
        with self.connection.cursor('dict') as cursor:
            cursor.execute(
                query,
                params
            )
            result = cursor.fetchone() or {}
            return result


class DuatRepository(metaclass=BaseRepositoryMetaclass):
    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def get_employee_email_by_code(self, employee_code: str):
        query = self.query_get_employee_email_by_code.format(
            schema_name=settings.postgres_duat.SCHEMA,
        )

        result = await self.connection.fetch(query, employee_code)

        if result:
            return result[0].get("email")

    async def get_employee_detail_by_code_or_phone(self, employee_code: str, trusted_phone_number: str):
        query = self.query_get_employee_detail_by_code_or_phone.format(
            schema_name=settings.postgres_duat.SCHEMA,
        )
        result = await self.connection.fetch(query, employee_code, trusted_phone_number)
        if result:
            return result[0]
        return None, None
