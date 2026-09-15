import json
import logging

import httpx
from asyncpg import Connection
from fastapi import APIRouter, Depends, Path, status
from fastapi.responses import JSONResponse

from app.api.statgov import service
from app.api.statgov.exceptions import company_404, error_429
from app.api.statgov.models import CompanyInformation, CompanyInformationAPI
from app.dependencies import get_collector_db, get_http_client
from app.providers import HTTPProvider

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/statgov", tags=["statgov"], default_response_class=JSONResponse)

# <editor-fold desc="Documentation">
examples = {
    'АО "НАРОДНЫЙ СБЕРЕГАТЕЛЬНЫЙ БАНК КАЗАХСТАНА"': {
        "summary": "Пример запроса по БИНу",
        "value": "940140000385",
    }
}

response = {
    "bin": "940140000385",
    "name": 'АО "НАРОДНЫЙ СБЕРЕГАТЕЛЬНЫЙ БАНК КАЗАХСТАНА"',
    "registerDate": "1994-01-20",
    "okedCode": "64192",
    "okedName": "Деятельность сберегательных банков",
    "secondOkeds": None,
    "krpCode": "311",
    "krpName": "Крупные предприятия (>1000)",
    "katoCode": "751710000",
    "katoDescription": "АЛМАТЫ Қ., МЕДЕУ АУДАНЫ",
    "legalAddress": "ПРОСПЕКТ АЛЬ-ФАРАБИ, 40",
    "owner": "ШАЯХМЕТОВА УМУТ БОЛАТХАНОВНА",
    "periodCode": None,
    "periodDate": "2023-02-01",
}

responses = {
    200: {
        "description": "Sample Description",
        "content": {
            "application/json": {
                "examples": {
                    "940140000385": {"value": response},
                }
            }
        },
    },
    404: {
        "description": "Company not found in the database.",
        "content": {
            "application/json": {
                "examples": {
                    "195ebd18-f459-4919-b89a-51bb5f037549": {
                        "value": {"detail": "Company not found in the database."}
                    }
                }
            }
        },
    },
}
# </editor-fold>


@router.get(
    "/{bin}",
    status_code=status.HTTP_200_OK,
    response_model=CompanyInformation,
    responses=responses,
)
async def fetch_company_data(
    bin: str = Path(..., description="БИН/ИИН компании", regex=r"^[\d]{12}$", examples=examples),
    conn: Connection = Depends(get_collector_db),
    async_client: HTTPProvider = Depends(get_http_client),
) -> CompanyInformation:
    record = await service.fetch_company_info(conn, biniin=bin)
    try:
        if record:
            return CompanyInformation(**record)
        else:
            r = await async_client.get(url=f"https://stat.gov.kz/api/juridical?bin={bin}&lang=ru")
            if r.status_code == 429:
                raise error_429
            elif r.status_code == 200:
                if r.json()["success"]:
                    raw = r.json()["obj"]

                    company_info = CompanyInformationAPI(
                        bin=raw["bin"],
                        name=raw["name"],
                        register_date=raw["registerDate"],
                        oked_code=raw["okedCode"],
                        oked_name=raw["okedName"],
                        second_okeds=raw["secondOkeds"],
                        krp_code=raw["krpCode"],
                        krp_name=raw["krpName"],
                        kato_code=raw["katoCode"],
                        kato_description=None,
                        legal_address=raw["katoAddress"],
                        owner=raw["fio"],
                        period_code=None,
                        period_date=None,
                    )
                    async with conn.transaction():
                        await service.insert_company_info(conn, company_info=company_info)
                    return company_info
                else:
                    raise company_404
            else:
                r.raise_for_status()
    except httpx.TimeoutException as timeout_error:
        logger.exception(msg=timeout_error)
        logger.error(
            f"Could not fetch company data from https://stat.gov.kz/api/juridical?bin={bin}&lang=ru due "
            f"to timeout error"
        )
        raise
    except json.JSONDecodeError as json_decode_error:
        logger.exception(msg=json_decode_error)
        raise
