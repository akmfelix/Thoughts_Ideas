from app.api.user_profile import models
from app.providers import GoszakupProvider


class ClientsHistoryGoszakupProvider(GoszakupProvider):
    async def get_id_from_biniin(self: "ClientsHistoryGoszakupProvider", supplier_bin: str) -> int | None:
        query_string = """
            query ($supplierBin: String!){
                Subjects (limit: 1, after: 0, filter: {bin: $supplierBin})
                {
                    pid
                }
            }
            """

        variables = {"supplierBin": supplier_bin}
        headers = {"Authorization": f"Bearer {self.token}"}

        res = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )

        res = res.json()
        subjects = res.get("data").get("Subjects")

        if subjects is None:
            return None

        return subjects[0].get("pid")

    async def get_suppliers_acts(
        self: "ClientsHistoryGoszakupProvider",
        supplier_id: int,
        after: int,
        limit: int,
    ) -> models.UserProfilesResponse:
        query_string = """
            query ($limit: Int!, $after: Int!, $supplierId: Int!) {
                Acts (limit: $limit, after: $after, filter: {supplierId: $supplierId}) {
                    id
                    aktDate
                    numberAct

                    createDateAct

                    contractRootId
                    contractRootId
                    statusId
                    isDeleted
                    dayOverdue

                    sumAvans
                    sumBeginning
                    sumFine
                    sumPreviously
                    sumTransfer

                    createDateGenInfo
                    statusNameRu
                    statusNameKz

                    supplierId
                    customerId

                    isGu
                    typeAct
                    refSubjectTypeId
                    parentId
                    systemId
                    indexDate

                    approveDate

                }
            }
        """

        variables = {"supplierId": supplier_id, "after": after, "limit": limit}
        headers = {"Authorization": f"Bearer {self.token}"}

        res = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )
        result = res.json()

        data = result.get("data")
        acts = models.acts.GoszakupActs(**data)

        next_page = result.get("extensions").get("pageInfo").get("lastId")

        return models.UserProfilesResponse(
            items=acts.acts,
            page=after,
            next_page=next_page,
        )

    async def get_suppliers_treasury_payments(
        self: "ClientsHistoryGoszakupProvider",
        supplier_bin: str,
        after: int,
        limit: int,
    ) -> models.UserProfilesResponse:
        query_string = """
               query ($limit: Int!, $after: Int!, $supplierBin: String!) {
               Contract (limit: $limit, after: $after, filter: {supplierBiin: $supplierBin})
                {
                    # supplierBiin

                    TreasuryPay {
                        id
                        nomZa
                        contractId
                        dtReg
                        nomUved
                        supplier
                        rnnSupplier
                        bikSupplier
                        iikSupplier
                        codeSupplier

                        nomDog   # Redundant?
                        dtDog  # Redundant?

                        itemDescription
                        quantity
                        unitPrice
                        nomDop
                        dtDop
                        typeBujet
                        budgetNameRu
                        budgetNameKz
                        kato
                        func
                        espk
                        gu
                        finSource
                        poHeaderId
                        lastUpdateDate
                        vendorId
                        pdiUpdateDate
                        prepaySum
                        strPrepaySum
                        checkId
                        invoiceId
                        payDescription
                        invnum
                        payAmount
                        checkNumber
                        payDate
                        codeCombinationId
                        ppn
                        accountingDate
                        indexDate
                        systemId
                        }
                    }
                }
           """

        variables = {"supplierBin": supplier_bin, "after": after, "limit": limit}
        headers = {"Authorization": f"Bearer {self.token}"}

        response = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )
        res = response.json()

        data = res.get("data")
        goszakup_contract = models.treasury_payments.GoszakupContract(**data)
        next_page = res.get("extensions").get("pageInfo").get("lastId")

        return models.UserProfilesResponse(
            items=goszakup_contract.contract,
            page=after,
            next_page=next_page,
        )

    async def get_suppliers_applications(
        self: "ClientsHistoryGoszakupProvider",
        supplier_bin: str,
        after: int,
        limit: int,
    ) -> models.UserProfilesResponse:
        query_string = """
               query ($limit: Int!, $after: Int!, $supplierBin: String!) {
               TrdApp (limit: $limit, after: $after, filter: {supplierBinIin: $supplierBin})
                {
                    supplierId,
                    supplierBinIin,
                    # protId,
                    # protNumber,

                    TrdBuy {
                        id

                        numberAnno  # Номер закупки
                        nameRu  # Наименование закупки
                        totalSum  # Общая сумма закупки (нужен 1 процент от этого поля)

                        countLots

                        # customerPid
                        customerNameRu  # БИН бенефициара
                        customerBin  # Наименование бенецифара


                        startDate  # дата начала закупки
                        endDate  # дата окончания закупки

                        status: RefBuyStatus {
                            id
                            nameRu
                            code

                        }

                        # buyType: RefTypeTrade {
                        # 	id
                        # 	nameRu
                        # 	nameKz
                        # }


                    }

                    lots: AppLots {
                        lot: Lot {
                            lotNumber,  # Номер лота
                            nameRu,  # Наименование лота
                            # descriptionRu,
                            # trdBuyNumberAnno,
                            count  # Общее кол-во
                            amount  # Общая сумма
                        }
                        ref: RefAppStatus {
                            id,
                            nameRu,  # Статус
                            code
                        }
                    }
                }
            }
           """

        variables = {"supplierBin": supplier_bin, "after": after, "limit": limit}
        headers = {"Authorization": f"Bearer {self.token}"}

        res = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )
        result = res.json()

        data = result.get("data")
        apps = models.applications.GoszakupApplications(**data)

        next_page = result.get("extensions").get("pageInfo").get("lastId")

        return models.UserProfilesResponse(
            items=apps.trd_app,
            page=after,
            next_page=next_page,
        )

    async def get_suppliers_contracts(
        self: "ClientsHistoryGoszakupProvider", supplier_bin: str, after: int, limit: int
    ) -> models.UserProfilesResponse:
        query_string = """
               query ($limit: Int!, $after: Int!, $supplierBin: String!) {
               Contract (limit: $limit, after: $after, filter: {supplierBiin: $supplierBin})
                {

                    supplierBiin

                    id
                    contractNumber  # Номер договора

                    contractSum  # Сумма заключенного контракта без ндс
                    contractSumWnds # Сумма заключенного контракта с ндс
                    faktSum  # Сумма фактических выплат без ндс
                    faktSumWnds  # Сумма фактических выплат c ндс


                    trdBuyNumberAnno  # Номер объявления
                    trdBuyNameRu  # Наименование объявления

                    crdate # Дата создания
                    signDate  # Дата подписания
                    contractEndDate # Дата завершения
                    ecEndDate  # Срок действия

                    descriptionRu  # Описание на русском языке

                    finYear  # Финансовый год

                    contractMs

                    # Статус договора
                    RefContractStatus {
                        nameRu
                        code
                    }

                    # Заказчик
                    customer: Customer {
                        bin
                        iin
                        customer
                        name
                        nameRu

                    }

                    trdBuy: TrdBuy {
                        # Тип закупки
                        buyType: RefTypeTrade {
                            id
                            nameRu
                            nameKz
                        }
                    }


                    contractType: RefContractType {
                        id
                        nameRu
                        nameKz
                    }

                    TreasuryPay {
                        payAmount
                        # id
                        # nomZa
                        # contractId
                        # dtReg
                        # nomUved
                        # supplier
                        # rnnSupplier
                    }
                }
            }
           """

        variables = {"supplierBin": supplier_bin, "after": after, "limit": limit}
        headers = {"Authorization": f"Bearer {self.token}"}

        res = await self.provider.execute(
            url=self.url,
            query=query_string,
            variables=variables,
            headers=headers,
        )
        result = res.json()
        data = result.get("data")
        contract = models.contracts.GoszakupContract(**data)

        next_page = result.get("extensions").get("pageInfo").get("lastId")

        return models.UserProfilesResponse(
            items=contract.contract,
            page=after,
            next_page=next_page,
        )
