from datetime import date
from typing import Any, Type, TypeVar

import asyncpg
import json
from pydantic import BaseModel

from app.api.profile import utils
from app.api.profile.models import (
    AverageDailyBalance, Payroll, NOITotal, NOIByProducts, ActualIncome,
    AccountTurnover, AverageTransactionTicket, AcquiringTurnover, AverageAcquiringTicket,
    QRTurnover, BNPLTurnover, CardPaymentTurnover, CashTransaction,
    CounterpartiesTop, OwnFundsPayeesTop, CreditApplicationAndGuarantee,
    Signatory, BeneficialOwner, Founder, SCFSupply, 
    WalletShareTurnover, WalletShareBalance, Margin, SupplyChainFinance, CreditApplicationStatus,
    TransfersToSTB
)
from app.repositories import BaseRepositoryMetaclass


T = TypeVar("T", bound=BaseModel)


class HermesRepository(metaclass=BaseRepositoryMetaclass):
    """Репозиторий для получения данных о профилях клиентов"""

    def __init__(self, connection: asyncpg.Connection):
        self.connection = connection

    async def get_average_daily_balance(
        self,
        biniin: str,
        start_date: date,
        end_date: date,
    ) -> list[AverageDailyBalance]:
        results = await self.connection.fetch(
            self.query_select_average_daily_balance,
            biniin,
            start_date,
            end_date,
        )

        return self._fill_missing_months(results, start_date, end_date, AverageDailyBalance)

    async def get_company_wage_fund(self, biniin: str) -> list[Payroll]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_cwf

        return [Payroll.parse_obj(cwf) for cwf in get_mock_cwf()]

    async def get_noi_total(self, biniin: str) -> list[NOITotal]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_noi_total

        return [NOITotal.parse_obj(noi) for noi in get_mock_noi_total()]

    async def get_noi_by_products(self, biniin: str) -> list[NOIByProducts]: 
        result = await self.connection.fetch(
            self.query_select_noi_by_products,
            biniin
        ) 

        return [
            NOIByProducts.parse_obj(json.loads(row['noi_data'])) 
            for row in result
        ]

    async def get_actual_income(self, biniin: str) -> list[ActualIncome]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_actual_income

        return [ActualIncome.parse_obj(el) for el in get_mock_actual_income()]

    async def get_account_turnover(self, biniin: str) -> list[AccountTurnover]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_account_turnover

        return [AccountTurnover.parse_obj(el) for el in get_mock_account_turnover()]

    async def get_average_transaction_ticket(self, biniin: str) -> list[AverageTransactionTicket]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_average_transaction_ticket

        return [AverageTransactionTicket.parse_obj(el) for el in get_mock_average_transaction_ticket()]

    async def get_acquiring_turnover(self, biniin: str) -> list[AcquiringTurnover]: 
        results = await self.connection.fetch(
            self.query_select_acquiring_turnover,
            biniin,
        )
        
        parsed_results = []
        for row in results:
            row_dict = dict(row) 
            if isinstance(row_dict["items"], str):
                row_dict["items"] = json.loads(row_dict["items"]) 
            parsed_results.append(AcquiringTurnover.parse_obj(row_dict))
            
        return parsed_results

    async def get_average_acquiring_ticket(self, biniin: str) -> list[AverageAcquiringTicket]: 
        results = await self.connection.fetch(
            self.query_select_average_acquiring_ticket,
            biniin,
        )

        return [AverageAcquiringTicket.parse_obj(dict(row)) for row in results]

    async def get_qr_turnover(self, biniin: str) -> list[QRTurnover]: 
        results = await self.connection.fetch(
        self.query_select_qr_turnover,
        biniin,
    )
    
        parsed_results = []
        for row in results:
            row_dict = dict(row)
            parsed_results.append(QRTurnover.parse_obj(row_dict))
            
        return parsed_results

    async def get_bnpl_turnover(self, biniin: str) -> list[BNPLTurnover]:
        results = await self.connection.fetch(
            self.query_select_bnpl_turnover,
            biniin,
        )

        parsed_results = []
        for row in results:
            row_dict = dict(row)
            parsed_results.append(BNPLTurnover.parse_obj(row_dict))
            
        return parsed_results


    async def get_card_payment_turnover(self, biniin: str) -> list[CardPaymentTurnover]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_card_payment_turnover

        return [CardPaymentTurnover.parse_obj(el) for el in get_mock_card_payment_turnover()]

    async def get_cash_transaction(self, biniin: str) -> list[CashTransaction]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_cash_transaction

        return [CashTransaction.parse_obj(el) for el in get_mock_cash_transaction()]

    async def get_transfers_to_stb(
        self,
        biniin: str
    ) -> TransfersToSTB:
        result = await self.connection.fetchrow(self.query_select_transfers_to_stb, biniin)
        result = result or {}

        result_model = TransfersToSTB.parse_obj(result)
        result_model.period_from = utils.get_month_date(2)
        result_model.period_to = utils.get_month_date(0)

        return result_model

    async def get_counterparties_top(self, biniin: str) -> CounterpartiesTop:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_counterparties_top

        return CounterpartiesTop.parse_obj(get_mock_counterparties_top())

    async def get_own_funds_payees_top(self, biniin: str) -> list[OwnFundsPayeesTop]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_own_funds_payees_top

        return [OwnFundsPayeesTop.parse_obj(el) for el in get_mock_own_funds_payees_top()]

    async def get_credit_application_and_guarantee(
        self,
        biniin: str
    ) -> list[CreditApplicationAndGuarantee]:
        results = await self.connection.fetch(
            self.query_select_credit_application_and_guarantee,
            biniin,
        )

        statuses = {
            "REJECTION": CreditApplicationStatus.REJECTED,
            "TIME_ELAPSED": CreditApplicationStatus.EXPIRED,
            "FULFILLED": CreditApplicationStatus.APPROVED,
            "IN_BRANCH": CreditApplicationStatus.PENDING,
        }
        formatted_results = []
        for result in results:
            result = dict(result)
            result["status"] = statuses[result["status"]]
            formatted_results.append(result)

        return [CreditApplicationAndGuarantee.parse_obj(el) for el in formatted_results]

    async def get_signatories(self, biniin: str) -> list[Signatory]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_signatories

        return [Signatory.parse_obj(el) for el in get_mock_signatories()]

    async def get_beneficial_owners(self, biniin: str) -> list[BeneficialOwner]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_beneficial_owners

        return [BeneficialOwner.parse_obj(el) for el in get_mock_beneficial_owners()]

    async def get_founders(self, biniin: str) -> list[Founder]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_founders

        return [Founder.parse_obj(el) for el in get_mock_founders()]

    async def get_wallet_share_turnover(self, biniin: str) -> WalletShareTurnover:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_wallet_share_turnover

        return WalletShareTurnover.parse_obj(get_mock_wallet_share_turnover())

    async def get_wallet_share_balance(self, biniin: str) -> WalletShareBalance:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_wallet_share_balance

        return WalletShareBalance.parse_obj(get_mock_wallet_share_balance())

    async def get_margin(self, biniin: str) -> list[Margin]:
        # MOCKED - То, что будет приходить из базы
        from .mock import get_mock_margin

        return [Margin.parse_obj(el) for el in get_mock_margin()]

    async def get_supply_chain_finance(self, biniin: str) -> SupplyChainFinance:
        result = SupplyChainFinance()

        result.anchors_count = await self.connection.fetch(
            self.query_select_supply_chain_finance_anchors_count,
            biniin 
        )

        result.anchors_top = [
            SCFSupply.parse_obj(el) for el in await self.connection.fetch(
                self.query_select_supply_chain_finance_top_anchors,
                biniin 
            )
        ]
        result.counterparties_count = await self.connection.fetch(
            self.query_select_supply_chain_finance_counterparties_count,
            biniin 
        )
        result.counterparties_top = [
            SCFSupply.parse_obj(el) for el in await self.connection.fetch(
                self.query_select_supply_chain_finance_top_counterparties,
                biniin 
            )
        ]

        return result

    @staticmethod
    def _fill_missing_months(
        data: list[dict[str, Any]],
        start_date: date,
        end_date: date,
        model: Type[T],
        date_field: str = "period",
    ) -> list[T]:
        """
        Заполняет отсутствующие месяцы в списке данных объектами модели с null значениями.
        """
        existing_data = {
            item[date_field]
            if isinstance(item[date_field], date)
            else item[date_field]: model.parse_obj(item) for item in data
        }

        full_period = utils.get_month_range(start_date, end_date)

        return [existing_data.get(dt) or model.parse_obj({date_field: dt}) for dt in full_period]
