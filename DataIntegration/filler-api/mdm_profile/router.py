import logging

from fastapi import APIRouter, Depends, Path, Request

from app.api.mdm_profile.dependencies import (
    MdmReposValidator,
    OcrmIdValidator,
    PublicIdValidator,
    _trusted_phone_number_validator
)
from app.api.mdm_profile.exceptions import NoQueryParams
from app.api.mdm_profile.models import AcquiringTurnover, HalykEmployee
from app.api.mdm_profile.repositories import DuatRepository
from app.dependencies import get_directus_http_client, get_duat_db
from app.providers import DirectusHttpProvider
from app.settings import get_settings

router = APIRouter(prefix="/mdm/profile", tags=["profile"])

logger = logging.getLogger()

settings = get_settings()


@router.get(
    "/ul/{biniin}/acquiring-turnover",
)
async def get_acquiring_turnover_by_biniin(
    mdm_repos: MdmReposValidator,
    biniin: str = Path(default=..., alias="biniin"),
):
    turnover: AcquiringTurnover = AcquiringTurnover(
        **{
            **await mdm_repos.get_acquiring_turnover_by_biniin(biniin),
            "biniin": biniin
        }
    )
    return turnover




@router.get(
    "/fl/check-employee",
)
async def get_halyk_employee_by_id(
    request: Request,
    ocrm_id: OcrmIdValidator,
    public_id: PublicIdValidator,
    mdm_repos: MdmReposValidator,
    async_client: DirectusHttpProvider = Depends(get_directus_http_client),
):
    if public_id is None and ocrm_id is None:
        raise NoQueryParams

    employee_info: HalykEmployee = HalykEmployee(
        **await mdm_repos.get_employee_by_ocrm_public_id(ocrm_id, public_id)
    )

    if not employee_info.is_employee and employee_info.trusted_phone_number is None:
        return employee_info
    
    employee_info.trusted_phone_number = _trusted_phone_number_validator(employee_info.trusted_phone_number)

    try:
        if not employee_info.is_employee and employee_info.trusted_phone_number is not None:

            directus_response = await async_client.get(
                url=settings.directus_url.format(phone=employee_info.trusted_phone_number)
            )
            directus_data = await directus_response.json()
            directus_data = directus_data.get("data", [])
            if directus_data:
                found_phone = directus_data[0].get("Value")
                if employee_info.trusted_phone_number == found_phone:
                    employee_info.is_employee = True
                    employee_info.employee_code = employee_info.trusted_phone_number
                    return employee_info
            return employee_info
    except Exception as e:
        logger.debug(e)

    gen = request.app.dependency_overrides[get_duat_db]()
    connection = await anext(gen)
    duat_repos = DuatRepository(connection=connection)

    employee_info.email, is_partner = await duat_repos.get_employee_detail_by_code_or_phone(
        employee_code=employee_info.employee_code,
        trusted_phone_number=employee_info.trusted_phone_number,
    )

    # В случае если мы изначально не уверены, что данный пользователь является сотрудником -> опираемся на is_partner
    employee_info.is_employee = max(employee_info.is_employee, is_partner)

    if employee_info.is_employee and employee_info.employee_code is None:
        employee_info.employee_code = employee_info.trusted_phone_number
    return employee_info
