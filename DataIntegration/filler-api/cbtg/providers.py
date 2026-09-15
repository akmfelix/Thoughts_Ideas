import asyncio
import json
import re
from collections.abc import Mapping
from typing import Any

from lxml import html
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

from app.api.cbtg.exceptions import (
    AdNotFound,
    FoundMoreThanOneAd,
    GoszakupAdBuyStatusNotAllowed,
    GoszakupAdTradeMethodNotAllowed,
    SamrukAdBuyStatusNotAllowed,
)
from app.api.cbtg.models import GoszakupTrdBuy, SamrukAd, SamrukLot, SkPharmacyAd
from app.api.cbtg.service_entities import SamrukApiConfig, SkPharmacyApiConfig
from app.infrastructure.http.graphql_transport import GraphQLHttpTransport
from app.infrastructure.http.transport import BaseHttpTransport, HttpResponse
from app.providers import AioHTTPProvider
from app.settings import HttpxClientSettings

tracer = trace.get_tracer(__name__)


class CBTGSamrukProvider:
    def __init__(
        self,
        http_transport: BaseHttpTransport,
    ) -> None:
        self._transport: BaseHttpTransport = http_transport
        self._api_config = SamrukApiConfig()

    async def _get_json(
        self, path: str, params: Mapping[str, str] | None = None, trace_enabled: bool = False
    ) -> dict[str, Any]:
        response: HttpResponse = await self._transport.get(
            path,
            query=params or {},
            trace_enabled=trace_enabled,
        )

        if response.status_code >= 400:
            error_msg = f"HTTP Error {response.status_code} from {path}"
            raise RuntimeError(f"{error_msg}: {response.text}")

        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Invalid JSON response from {path}: {e}")

    async def _fetch_ad_and_lots(
        self, ad_number: str, trace_enabled: bool = False
    ) -> tuple[dict, dict]:
        ad_params = {"advert_number": ad_number}
        lot_params = {
            "advert_number": ad_number,
            "size": str(self._api_config.default_lot_size),
        }

        ad_task = self._get_json(
            self._api_config.search_advert_path, ad_params, trace_enabled=trace_enabled
        )
        lot_task = self._get_json(
            self._api_config.search_lot_path, lot_params, trace_enabled=trace_enabled
        )

        ad_data, lot_data = await asyncio.gather(ad_task, lot_task)
        return ad_data, lot_data

    async def get_ad(self, ad_number: str) -> SamrukAd:
        span = trace.get_current_span()
        span.set_attribute("ad_number", ad_number)
        span.set_attribute("config.search_advert_path", self._api_config.search_advert_path)
        span.set_attribute("config.search_lot_path", self._api_config.search_lot_path)

        span.add_event("business_logic_started", attributes={"ad_number": ad_number})
        try:
            ad_data, lot_data = await self._fetch_ad_and_lots(ad_number, trace_enabled=True)

            advertisements = ad_data.get("content", [])
            if not advertisements:
                span.set_status(Status(StatusCode.ERROR, "Ad not found in content"))
                raise AdNotFound

            published_ads = [ad for ad in advertisements if ad.get("advert_status") == "PUBLISHED"]
            if not published_ads:
                span.set_status(Status(StatusCode.ERROR, "No published ads found"))
                raise SamrukAdBuyStatusNotAllowed

            if len(published_ads) > 1:
                span.set_status(Status(StatusCode.ERROR, "Multiple published ads found"))
                raise FoundMoreThanOneAd

            advertisement = published_ads[0]
            lots_content = lot_data.get("content", [])

            lots = [
                SamrukLot(
                    id=lot["lot_id"],
                    name=lot["lot_name"],
                    amount=lot["sum_no_nds"],
                    ad_number=lot["advert_number"],
                    status_code=lot["lot_status"],
                )
                for lot in lots_content
                if lot.get("lot_status") == "PUBLISHED"
            ]

            result = SamrukAd(
                number=ad_number,
                name=advertisement["advert_name"],
                beneficiary_bin=advertisement["company_bin"],
                beneficiary_name=advertisement["company_name"],
                start_date=advertisement["advert_begin_time"],
                end_date=advertisement["advert_end_time"],
                status_code=advertisement["advert_status"],
                lots=lots,
            )

            span.set_attribute("result.lots_count", len(lots))
            span.set_status(Status(StatusCode.OK))

            return result

        except Exception as e:
            span.record_exception(e)
            if span.status.status_code == StatusCode.UNSET:
                span.set_status(Status(StatusCode.ERROR, str(e)))
            raise

    async def get_ad_details(self, ad_id: int) -> dict[str, Any]:
        response_data = await self._get_json(
            self._api_config.search_advert_path,
            {"advert_number": str(ad_id)},
        )

        if "fieldErrors" in response_data:
            raise AdNotFound

        documents = response_data.get("documents", [])
        tender_docs = [
            el.get("fileUid")
            for el in documents
            if el.get("documentCategory") == "TENDER_DOCUMENTATION"
        ]

        keys_to_extract = {
            "number",
            "nameRu",
            "organizer",
            "acceptanceBeginDateTime",
            "acceptanceEndDateTime",
            "advertStatus",
        }

        result = {key: response_data.get(key) for key in keys_to_extract}
        result["tenderDocFileUid"] = tender_docs[0] if tender_docs else None
        return result

    async def get_ad_lots(self, ad_number: str) -> dict[str, list[dict]]:
        params = {"advert_number": ad_number, "size": str(self._api_config.default_lot_size)}
        response_content = await self._get_json(
            self._api_config.search_lot_path,
            params,
        )

        lots_list = (
            response_content
            if isinstance(response_content, list)
            else response_content.get("content", [])
        )

        return {
            "lots": [
                {
                    "adNumber": ad_number,
                    "id": lot["lot_id"],
                    "nameRu": lot["lot_name"],
                    "sumTruNoNds": lot["sum_no_nds"],
                    "lotStatus": lot["lot_status"],
                }
                for lot in lots_list
                if lot.get("lot_status") == "PUBLISHED"
            ]
        }


class CBTGGoszakupProvider:
    def __init__(self, graphql_transport: GraphQLHttpTransport) -> None:
        self._transport = graphql_transport

    async def get_ad(self, ad_number: str):
        query = """
            query ($adNumber: String!){
                TrdBuy (filter: {numberAnno: $adNumber}) {
                    adNumber: numberAnno,
                    adName: nameRu,
                    beneficiaryBin: orgBin,
                    beneficiaryName: orgNameRu,
                    startDate: startDate,
                    endDate: endDate,
                    repeatStartDate,
                    repeatEndDate,
                    lots: Lots {
                        lotNumber: lotNumber,
                        lotName: nameRu,
                        amount: amount,
                        status: RefLotsStatus {
                            statusName: nameRu,
                            statusCode: code
                        },
                        adNumber: trdBuyNumberAnno
                    },
                    status: RefBuyStatus {
                        statusName: nameRu,
                        statusCode: code
                    },
                    tradeMethod: RefTradeMethods {
                        tradeMethodId: id
                        tradeMethodName: nameRu
                    }
                }
            }
        """

        variables = {"adNumber": ad_number}
        response = await self._transport.execute_query(
            url="/v3/graphql",
            query=query,
            variables=variables,
        )
        ads = response.json()["data"]["TrdBuy"]  # type: ignore
        if ads is None:
            raise AdNotFound
        if len(ads) > 1:
            raise FoundMoreThanOneAd

        ad: GoszakupTrdBuy = ads[0]
        return ad


class SkPharmacyProvider:
    def __init__(self, settings: HttpxClientSettings):
        self.provider = AioHTTPProvider(settings=settings)
        self._api_config = SkPharmacyApiConfig()

    async def get_ad(self, ad_number: str):
        ad_url, page_count = await self.get_ad_meta(ad_number=ad_number)
        ad_details = asyncio.create_task(self.get_final_ad(ad_url))
        ad_lots = asyncio.create_task(self.get_lots(ad_url, page_count, ad_number=ad_number))

        await ad_details
        await ad_lots

        ad = SkPharmacyAd(**{**ad_details.result(), **ad_lots.result()})

        return ad

    async def get_ad_meta(self, ad_number):
        res = await self.provider.get(self._api_config.ad_meta_url.format(ad_number))
        tree = html.fromstring(await res.text())
        tables = tree.xpath('.//table[contains(@class, "table")]')
        if not len(tables):
            raise AdNotFound
        table, *_ = tables

        if len(table) > 2:
            raise FoundMoreThanOneAd

        meta_data = {}
        for idx, header in enumerate(table.iter("th")):
            value, *_ = table.xpath(f"//tr[2]//td[{idx + 1}]/text()")
            meta_data[header.text.strip()] = (value.strip(),)

        _, _, ad_link, _ = next(table.iterlinks())
        if meta_data["Статус"][0] not in [
            "Опубликовано (прием заявок)",
            "Опубликовано (дополнение заявок)",
        ]:
            raise GoszakupAdBuyStatusNotAllowed
        if (
            meta_data["Способ закупки"][0]
            == "Конкурс на заключение долгосрочных договоров поставки ЛС и МИ"
        ):
            raise GoszakupAdTradeMethodNotAllowed
        return self._api_config.ad_base_url + ad_link, int(meta_data["Кол-во лотов"][0])

    async def get_lots(self, url, count_lots, ad_number):
        lots_data, tasks = [], []
        semaphore = asyncio.Semaphore(50)
        count_page = (count_lots + 19) // 20

        for page in range(1, count_page + 1):
            task_lot_meta = asyncio.create_task(self.get_lots_metadata(url, page, semaphore))
            tasks.append(task_lot_meta)

        lot_meta_results = await asyncio.gather(*tasks)
        for meta_result in lot_meta_results:
            fields_indices = meta_result["fields_indices"]
            for row in meta_result["rows"]:
                lot = self.parse_lot(row=row, fields_indices=fields_indices, ad_number=ad_number)
                lots_data.append(lot)

        return {"lots": lots_data}

    async def get_lots_metadata(self, url, page, semaphore):
        async with semaphore:
            res = await self.provider.get(url + f"?tab=lots&page={page}")
        tree = html.fromstring(await res.text())
        table, *_ = tree.xpath('.//table[contains(@class, "table")]')
        headers = table.iter("th")
        headers = [th.text for th in headers]
        rows = list(table.iter("tr"))
        rows = rows[1:]
        fields_indices = {}
        for field, possible_names in self._api_config.mapping_lots_fields.items():
            for name in possible_names:
                if name in headers:
                    fields_indices[field] = headers.index(name)
                    break
        return {"headers": headers, "rows": rows, "fields_indices": fields_indices}

    def parse_lot(self, row, fields_indices, ad_number):
        row_data = {}
        for field, index in fields_indices.items():
            cells = row.getchildren()
            value = cells[index].text_content()
            row_data[field] = value.strip() if value else None
        row_data["adNumber"] = ad_number
        return row_data

    async def get_final_ad(self, url):
        res = await self.provider.get(url + "?tab=general")
        tree = html.fromstring(await res.text())
        ad_organizer = await self.get_ad_organizer(tree)
        ad_header_info = await self.get_ad_header(tree)
        ad = ad_organizer | ad_header_info
        return ad

    async def get_ad_organizer(self, tree):
        table, *_ = tree.xpath('.//table[contains(@class, "table")]')
        ad = {}
        for header, value in table.iter("tr"):
            if (
                header.text
                and value.text
                and header.text in self._api_config.headers_organizer_field
            ):
                organizer = value.text
                organizer_split = re.match(r"(\d{12})\s*(.*)", organizer)
                ad["beneficiaryBin"] = organizer_split.group(1)  # type: ignore
                ad["beneficiaryName"] = organizer_split.group(2)  # type: ignore
            # if (
            #        header.text
            #        and value.text
            #        and header.text in ["Способ проведения закупки"]
            # ):
            #    ad["adMethod"] = value.text
        return ad

    async def get_ad_header(self, tree):
        ad = {}
        rows = tree.xpath('//div[contains(@class,"form-group")]')
        for row in rows:
            header = row.text_content().strip()
            value = row.xpath("div//input/@value")
            for key in self._api_config.headers_ad_fields.keys():
                if header and value and header == key:
                    ad[self._api_config.headers_ad_fields[key]] = value[0]
        return ad
