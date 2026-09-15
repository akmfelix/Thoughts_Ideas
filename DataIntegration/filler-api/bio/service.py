from asyncpg import Connection

from app.api.bio.models import TreasuryPay


async def get_details_by_id_or_number(
    conn: Connection, contract_id: str | None = None, contract_number: str | None = None
):
    parameter = None
    query = """
        SELECT
            "absenceSecurityPerformanceContract",
            "securityDepositTotalAmountContract",
            "bankGuaranteeAmountInAccordanceLaw26",
            "cashGuaranteeAmountInAccordanceLaw26",
            "ewalletCollateralMoney3percentContractAmount",
            "ewalletMoneyAmountInAccordanceLaw26",
            "bankGuaranteeAmountInAdvanceUnderContract",
            "civilLiabilityInsurance3percentTotalContractAmount",
            "bankGuarantee3percentTotalContractAmount"
        FROM public.goszakup_contract_enforcements where "{}" = $1;
    """

    if contract_id is None:
        query = query.format("contract_number")
        parameter = contract_number

    elif contract_number is None:
        query = query.format("pid")
        parameter = int(contract_id)

    result_set = await conn.fetch(query, parameter)
    return result_set


async def get_treasury_pay_received_payments(
    conn: Connection,
    biniin: str,
) -> list[TreasuryPay]:
    query = """
        SELECT
              bik_supplier
            , sum(pay_amount) as "pay_amount"
            , to_char(pay_date, 'YYYY-MM') as "pay_month"
            , count(1) as "pay_quantity"
        FROM public.goszakup_treasury_pay
        WHERE
            pay_date between current_date - interval '2 year' and current_date
            AND rnn_supplier=$1
        GROUP BY bik_supplier, to_char(pay_date, 'YYYY-MM')
    """

    records = await conn.fetch(query, biniin)
    treasury_pays = [TreasuryPay(**r) for r in records]

    return treasury_pays
