import re
from typing import Annotated

from fastapi import Depends

from app.api.mvp.models import SystemTypes
from app.exceptions import ValidationError


def _system_type_validator(system_type: str):
    try:
        return SystemTypes(system_type)
    except ValueError:
        raise ValidationError("System Type Value Not Allowed")


# 150140011503
def _client_id_validator(
    biniin: str | None = None,
    colvir: str | None = None,
) -> str:
    client_id: str = biniin if biniin is not None else colvir

    if client_id is None:
        raise ValidationError("Client ID was not provided")

    regex = r"^[\d]{12}$" if biniin is not None else r"^\d{6,6}\.\d{6,6}\s*$"

    if not re.match(regex, client_id):
        raise ValidationError("Client ID is not valid")

    return client_id


# 150140011503
def _client_id_type(
    biniin: str | None = None,
    colvir: str | None = None,
) -> str:
    if biniin is not None:
        return "biniin"
    elif colvir is not None:
        return "client_code"


systemTypeValidator = Annotated[str, Depends(_system_type_validator)]
clientIdValidator = Annotated[str, Depends(_client_id_validator)]
clientIdType = Annotated[str, Depends(_client_id_type)]
