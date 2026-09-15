import os
from collections import defaultdict
from datetime import date, datetime
from functools import cache

from app.api.mvp.models import MVPFuture, MVPIncome, MVPUserAttributes
from app.dependencies import Connection

if os.getenv("API_MODE") == "TEST":
    mvp_incomes_tablename = "filler_mvp_service_incomes_new"
else:
    mvp_incomes_tablename = "filler_mvp_service_incomes"


mvp_incomes_curr_month_tablebname = "filler_mvp_service_incomes_current_month"
mvp_futures_tablename = "filler_mvp_service_futures"
mvp_user_attributes_tablename = "filler_mvp_service_user_attribute"


@cache
def gen_history_dates_between(start: str, end: str) -> dict[str, int]:
    """Generates dict of dates between two points

    Args:
        start: str of date in format "yyyy-mm"
        end: str of date in format "yyyy-mm"

    Returns:
        Dictionary key=date value=0

    """
    start_year, start_month = start.split("-")
    end_year, end_month = end.split("-")

    start_date = date(int(start_year), int(start_month), 1)
    end_date = date(int(end_year), int(end_month), 1)

    if start_date < end_date:
        start_date, end_date = end_date, start_date

    dates = {}

    while start_date >= end_date:
        dates[start_date.strftime("%Y-%m")] = 0
        if start_date.month - 1 > 0:
            start_date = start_date.replace(month=(start_date.month - 1))
        else:
            start_date = start_date.replace(year=start_date.year - 1, month=12)

    return dates


async def get_mvp_incomes(
    system_name: str,
    client_id: str,
    client_id_type: str,
    conn: Connection,
):
    records = await conn.fetch(
        f"""
            SELECT BINIIN, CLIENT_CODE, SYSTEM_NAME, PRODUCT_CATEGORY_ID, PRODUCT_CODE, PRODUCT_NAME, INCOME, DATE_BY_MONTH, LOAD_DATE FROM {mvp_incomes_tablename} WHERE system_name = $1 AND {client_id_type} = $2
            UNION ALL
            SELECT BINIIN, CLIENT_CODE, SYSTEM_NAME, PRODUCT_CATEGORY_ID, PRODUCT_CODE, PRODUCT_NAME, INCOME, DATE_BY_MONTH, LOAD_DATE FROM {mvp_incomes_curr_month_tablebname} WHERE system_name = $1 AND {client_id_type} = $2
        """,
        system_name,
        client_id,
    )

    today = datetime.today().strftime("%Y-%m")

    history_range = 2  # years
    end_year = int(today.split("-")[0]) - history_range
    end_date = f"{end_year}-01"

    dates = gen_history_dates_between(today, end_date)

    res = defaultdict(lambda: defaultdict(dict))

    for r in records:
        income = MVPIncome(**r)
        if not res[income.product_category_id][income.product_code].get("incomes"):
            res[income.product_category_id][income.product_code]["incomes"] = {
                d: dates[d] for d in dates
            }

        res[income.product_category_id][income.product_code]["incomes"][
            income.date_by_month.strftime("%Y-%m")
        ] = income.income

    return res


async def get_mvp_futures(
    system_name: str,
    client_id: str,
    client_id_type: str,
    conn: Connection,
):
    records = await conn.fetch(
        f"""
            SELECT *
            FROM {mvp_futures_tablename}
            WHERE system_name = $1 AND {client_id_type} = $2
        """,
        system_name,
        client_id,
    )

    res = defaultdict(lambda: defaultdict(dict))

    for r in records:
        future = MVPFuture(**r)

        res[future.product_category_id][future.product_code]["future"] = future.future

    return res


async def log_manager(tabel_id: str, client_id: str, message: str, conn: Connection):
    async with conn.transaction():
        await conn.execute(
            """
                insert into public.mvp_manager_log("TABEL", "CLIENT_ID", "RESPONSE")
                values ($1, $2, $3)
            """,
            tabel_id,
            client_id,
            message,
        )


async def get_user_attributes(
    biniin: str,
    conn: Connection,
) -> dict | None:
    record = await conn.fetchrow(
        f"""
            SELECT is_high_profit_client
            FROM {mvp_user_attributes_tablename}
            where biniin = $1
        """,
        biniin,
    )
    if record is None:
        user_attributes = MVPUserAttributes()
    else:
        user_attributes = MVPUserAttributes(**dict(record))

    return user_attributes.dict(by_alias=True)
