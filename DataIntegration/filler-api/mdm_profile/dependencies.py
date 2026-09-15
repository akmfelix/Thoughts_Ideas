import re
from typing import Annotated

from fastapi import Depends, Query

from app.api.mdm_profile.repositories import MDMrepository
from app.dependencies import Connection, get_profile_connection
from app.exceptions import ValidationError


def _ocrm_id_validator(
    ocrm_id: str | None = Query(None, alias="ocrmId"),
) -> str | None:
    regex = r"^(?:\{|CL_{)[A-Za-z0-9-]{34,40}\}$"

    if ocrm_id is not None and not re.match(regex, ocrm_id):
        raise ValidationError("Ocrm Id is not valid", status_code=200)

    return ocrm_id


def _public_id_validator(
    public_id: str | None = Query(None, alias="publicId"),
) -> str | None:
    regex = r"^[A-Za-z0-9-]{34,40}$"

    if public_id is not None and not re.match(regex, public_id):
        raise ValidationError("Public Id is not valid", status_code=200)

    return public_id


def _mdmrepos_validator(
    connection: Connection = Depends(get_profile_connection)
) -> MDMrepository:
    mdm_repos = MDMrepository(connection=connection)
    return mdm_repos


def _trusted_phone_number_validator(
    trusted_phone_number: str | None = Query(None, alias="trustedPhoneNumber"),
) -> str | None:
    
    if trusted_phone_number is None or "|" in trusted_phone_number:
        return trusted_phone_number

    match = re.match(r"^7([0-9]{10})$", trusted_phone_number)
    if match:
        return match.group(1)
    
    return trusted_phone_number


OcrmIdValidator = Annotated[str, Depends(_ocrm_id_validator)]
PublicIdValidator = Annotated[str, Depends(_public_id_validator)]
MdmReposValidator = Annotated[MDMrepository, Depends(_mdmrepos_validator)]
