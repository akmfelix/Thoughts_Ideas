from fastapi import APIRouter, Depends
from mergedeep import merge as deepmerge

from app.api.mvp import service
from app.api.mvp.dependencies import (
    clientIdType,
    clientIdValidator,
    systemTypeValidator
)
from app.api.mvp.models import MVPResponse
from app.dependencies import Connection, get_collector_db
from app.exceptions import FillerHTTPException
from app.utils import set_timeout

router = APIRouter(prefix="/mvp", tags=["mvp"])


@router.get(
    "/{system_type}",
    # response_model=MVPResponse,
)
@set_timeout(
    milliseconds=50_000,
)
async def get_mvp(
    system_type: systemTypeValidator,
    client_id: clientIdValidator,
    client_id_type: clientIdType,
    tabel_id: str | None = None,
    conn: Connection = Depends(get_collector_db),
):
    msg = "success empty"
    try:
        user_attributes = dict()
        if "." not in client_id:
            user_attributes = await service.get_user_attributes(client_id, conn)

        mvp_incomes = await service.get_mvp_incomes(
            system_type,
            client_id,
            client_id_type,
            conn,
        )

        mvp_futures = await service.get_mvp_futures(
            system_type,
            client_id,
            client_id_type,
            conn,
        )
        res = deepmerge({}, mvp_incomes, mvp_futures)
        msg = "success"
        if len(res) == 0:
            msg += " empty"

        return {"userAttributes": user_attributes, "userProducts": res}
    except Exception as e:
        print(e)
        msg = "error"
        raise FillerHTTPException()
    finally:
        if tabel_id:
            await service.log_manager(tabel_id, client_id, msg, conn)


@router.get(
    "/{system_type}/incomes",
    response_model=MVPResponse,
    response_model_exclude_none=True,
)
@set_timeout(
    milliseconds=20_000,
)
async def get_mvp_incomes(
    system_type: systemTypeValidator,
    client_id: clientIdValidator,
    client_id_type: clientIdType,
    conn: Connection = Depends(get_collector_db),
):
    mvp_incomes = await service.get_mvp_incomes(
        system_type,
        client_id,
        client_id_type,
        conn,
    )

    return mvp_incomes


@router.get(
    "/{system_type}/futures",
    response_model=MVPResponse,
    response_model_exclude_none=True,
)
@set_timeout(
    milliseconds=20_000,
)
async def get_mvp_futures(
    system_type: systemTypeValidator,
    client_id: clientIdValidator,
    client_id_type: clientIdType,
    conn: Connection = Depends(get_collector_db),
):
    mvp_futures = await service.get_mvp_futures(
        system_type,
        client_id,
        client_id_type,
        conn,
    )

    return mvp_futures
