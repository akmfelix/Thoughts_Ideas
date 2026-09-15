from asyncpg import Connection, Record

from app.api.statgov import utils
from app.api.statgov.models import CompanyInformation


async def fetch_company_info(conn: Connection, biniin: str) -> Record:
    query = """
        SELECT
            biniin as "bin"
            , nameru as "name"
            , datereg as "register_date"
            , okedcode as "oked_code"
            , okedru as "oked_name"
            , okedcode2 as "second_okeds"
            , krpcode as "krp_code"
            , krpru as "krp_name"
            , kato as "kato_code"
            , katoru as "kato_description"
            , address as "legal_address"
            , owner as "owner"
            , period as "period_code"
            , date_period as "period_date"
        FROM public.statgov_actual_client_info
        WHERE BINIIN = $1
    """
    return await conn.fetchrow(query, biniin)


async def insert_company_info(conn: Connection, company_info: CompanyInformation):
    query = f"""
        insert into public.statgov_actual_client_info
        VALUES ({", ".join(f'${i}' for i in range(1, 15))})
    """
    await conn.execute(query, *utils.prepare_data(company_info))
