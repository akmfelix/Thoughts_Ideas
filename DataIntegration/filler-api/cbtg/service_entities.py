from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SamrukApiConfig:
    search_advert_path: str = "/data/second-tier-bank/searchbyadvert"
    search_lot_path: str = "/data/second-tier-bank/searchlotbyadvert"
    default_lot_size: int = 100


@dataclass(frozen=True)
class GoszakupApiConfig: ...


@dataclass(frozen=True, slots=True)
class SkPharmacyApiConfig:
    ad_base_url: str = "https://fms.ecc.kz"
    ad_meta_url: str = "https://fms.ecc.kz/ru/searchanno?numberAnno={}"

    headers_organizer_field: list[str] = field(
        default_factory=lambda: ["Единый дистрибьютор", "Организатор"]
    )

    headers_ad_fields: dict[str, str] = field(
        default_factory=lambda: {
            "Номер объявления": "number",
            "Наименование объявления": "nameRu",
            "Статус объявления": "advertStatus",
            "Срок начала приема заявок": "acceptanceBeginDateTime",
            "Срок окончания приема заявок": "acceptanceEndDateTime",
            "Срок начала приема дополнения заявок": "repeatStartDate",
            "Срок окончания приема дополнения заявок": "repeatEndDate",
        }
    )

    mapping_lots_fields: dict[str, Any] = field(
        default_factory=lambda: {
            "id": ["№ лота"],
            "nameRu": [
                "Наименование",
                "Наименование лота",
                "Форма/Вид медицинской помощи",
                "Наименование лекарственного средства и медицинских изделий по международному непатентованному наименованию",
                "МНН",
            ],
            "sumTruNoNds": ["Сумма", "Цена ЕД для закупа", "Общая сумма закупа (в тенге)"],
            "lotStatus": ["Статус", "Статус лота"],
        }
    )
