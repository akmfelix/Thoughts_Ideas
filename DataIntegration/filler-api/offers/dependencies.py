import re
from typing import Annotated

from fastapi import Depends, Path

from app.api.offers.models import SystemTypes
from app.exceptions import ValidationError


def _system_type_validator(system_type: str):
    try:
        return SystemTypes(system_type).value
    except ValueError:
        raise ValidationError("System Type Value Not Allowed")


def _client_id_validator(
    client_id: str = Path(..., alias="clientId"),
) -> str:
    if client_id is None:
        raise ValidationError("Client ID was not provided")

    regex = r"^\d{6,6}\.\d{6,6}\s*$"

    if not re.match(regex, client_id):
        raise ValidationError("Client ID is not valid")

    return client_id


systemTypeValidator = Annotated[str, Depends(_system_type_validator)]
clientIdValidator = Annotated[str, Depends(_client_id_validator)]
