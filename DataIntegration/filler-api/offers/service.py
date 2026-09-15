from asyncpg import Connection

from app.api.offers.models import GetOfferResponse

offers_table = "filler_mvp_service_futures"
offers_activated_table = "filler_offer_activated"


async def get_offers_by_client_id(system_name: str, client_code: str, conn: Connection):
    query = """
        with user_offers as (
            select OFFER_ID,PRODUCT_CODE,PRODUCT_NAME PRODUCT_DIRECTION,VALIDITY,CACHEPERIOD,ROLES
            from public.filler_mvp_service_futures
            where SYSTEM_NAME = $1
            and client_code = $2
            union all
            select OFFER_ID,PRODUCT_CODE,PRODUCT_NAME PRODUCT_DIRECTION,VALIDITY,CACHEPERIOD,ROLES
            from public.filler_offer_campaign_banner
            where SYSTEM_NAME = $1
            and client_code = $2
        )
        select uo.OFFER_ID, uo.PRODUCT_CODE, uo.PRODUCT_DIRECTION, uo.VALIDITY, uo.CACHEPERIOD, uo.ROLES 
        from user_offers uo 
        LEFT JOIN public.filler_offer_activated ac
            ON ac.system_name = $1 AND ac.client_code = $2 AND uo.offer_id=ac.offer_id
        where ac.client_code is null
    """
    data = await conn.fetch(query, system_name, client_code)

    return GetOfferResponse(data=data)


async def delete_and_log_activated_offers(
    system_name: str,
    product_direction: str,
    activated_offers: list[str],
    conn: Connection,
):
    activated_offers = [[off] if type(off) == str else off for off in activated_offers]

    async with conn.transaction():
        query = """
            insert into public.filler_offer_activated
            with user_offers as (
                select system_name, client_code, offer_id, product_code, product_name PRODUCT_DIRECTION, CURRENT_DATE AS CREATION_DATE
                from public.filler_mvp_service_futures
                where SYSTEM_NAME = $1
                and client_code = any($2::varchar[])
                union all
                select system_name, client_code, offer_id, product_code, product_name PRODUCT_DIRECTION, CURRENT_DATE AS CREATION_DATE
                from public.filler_offer_campaign_banner
                where SYSTEM_NAME = $1
                and client_code = any($2::varchar[])
            ) select uo.system_name, uo.client_code, uo.offer_id, uo.product_code, uo.PRODUCT_DIRECTION, uo.CREATION_DATE
            from user_offers uo
            LEFT JOIN public.filler_offer_activated ac
                ON ac.system_name = uo.system_name AND ac.client_code = uo.client_code
            where uo.SYSTEM_NAME = $1
            and uo.PRODUCT_DIRECTION = $3
            and uo.client_code = any($2::varchar[])
            and ac.client_code is null
        """
        await conn.execute(query, system_name, activated_offers, product_direction)
