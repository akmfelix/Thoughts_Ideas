from fastapi import APIRouter, Depends

from app.api.offers import service
from app.api.offers.dependencies import clientIdValidator, systemTypeValidator
from app.api.offers.models import (
    ActivatedOffers,
    GetOfferResponse,
    OfferInterest
)
from app.base import FillerResponse
from app.dependencies import (
    Connection,
    KafkaProducer,
    get_collector_db,
    get_producer
)
from app.utils import set_timeout

router = APIRouter(prefix="/offers", tags=["offers"])


@router.get(
    "/{system_type}/{clientId}",
    response_model=GetOfferResponse,
)
@set_timeout(
    milliseconds=1_000,
    default_response=FillerResponse(
        content={"data": []},
        status_code=200,
    ),
)
async def get_client_tariffs(
    system_type: systemTypeValidator,
    client_id: clientIdValidator,
    conn: Connection = Depends(get_collector_db),
    producer: KafkaProducer = Depends(get_producer),
):
    offers = await service.get_offers_by_client_id(
        system_type,
        client_id.strip(),
        conn=conn,
    )
    for offer in offers.data:
        producer.produce(offer.dict(by_alias=True), topic="ob-offer")
    return offers


@router.post("/{system_type}/interest")
@set_timeout(
    milliseconds=500,
)
async def fill_offer_interest(
    system_type: systemTypeValidator,
    offer_interest: OfferInterest,
    producer: KafkaProducer = Depends(get_producer),
):
    msg = offer_interest.dict(by_alias=True) | {"systemType": system_type}
    producer.produce(msg, topic="offers-interest")
    return msg


@router.delete("/{system_type}")
@set_timeout(
    milliseconds=1_000,
)
async def delete_activated_in_systemType(
    system_type: systemTypeValidator,
    activated_offers: ActivatedOffers,
    conn: Connection = Depends(get_collector_db),
):
    await service.delete_and_log_activated_offers(
        system_type,
        activated_offers.type,
        activated_offers.data,
        conn,
    )
