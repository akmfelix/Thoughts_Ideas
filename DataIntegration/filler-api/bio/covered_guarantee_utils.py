import asyncio
import logging
import re
from collections import deque
from typing import Literal

import pymupdf
from lxml import html

from app.exceptions import ExternalServiceUnavailable
from app.providers import DirectusHttpProvider, HTTPProvider

logger = logging.getLogger()

PERCENT_AMOUNT_PATTERN = r"(?:3|три|трех|трёх|5|пять|пяти)"
SPACE_PATTERN = r"[ \u00a0\n\r]"  # \u00a0 - NBSP (неразрывный пробел) в юникоде, обычно он используется в пдфках, чтобы число не разорвалось переносом строки между группами
PERCENT_PATTERN = (
    rf"(?:"
    rf"{PERCENT_AMOUNT_PATTERN}\s*(?:\(\s*{PERCENT_AMOUNT_PATTERN}\s*\))?"
    rf"|\(\s*{PERCENT_AMOUNT_PATTERN}\s*\)\s*{PERCENT_AMOUNT_PATTERN}"
    rf")"
    r"\s+процент(?:ов|а)?"
)
NUMBER_PATTERN = (
    r"\d+(?:" + SPACE_PATTERN + r"+\d+)*"
    r"(?:\s*[.,]\s*\d+(?:" + SPACE_PATTERN + r"+\d+)*)?"
    r"(?!\d)"
)

# ADVANCE_PATTERN = re.compile(
#     r"размеров\s+аванса"
#     r".{0,300}?"
#     r"равную\s+"
#     rf"({NUMBER_PATTERN})"
#     r"(?:\s*тенге)?",
#     re.IGNORECASE | re.DOTALL,
# )

ADVANCE_PATTERN = re.compile(
    r"обеспечени[еяю]\s+исполнени[еяю]\s+договора"
    r".{0,200}?"
    r"в\s+размере\s+" + PERCENT_PATTERN + r".{0,200}?"
    r"равную\s+" + NUMBER_PATTERN + r"(?:\s*тенге)?"
    r".{0,300}?"
    r"размеров\s+аванса"
    r".{0,300}?"
    r"равную\s+"
    rf"({NUMBER_PATTERN})"
    r"(?:\s*тенге)?",
    re.IGNORECASE | re.DOTALL,
)

ANTIDUMPING_PATTERN = re.compile(
    r"сумму\s+в\s+соответствии\s+со\s+(?:стать[её]й|статьи)\s+13\s+закона"
    r".{0,200}?"
    r"равную\s+"
    rf"({NUMBER_PATTERN})"
    r"(?:\s*тенге)?",
    re.IGNORECASE | re.DOTALL,
)

OBLIGATIONS_PATTERN = re.compile(
    r"обеспечени[еяю]\s+исполнени[еяю]\s+договора"
    r".{0,200}?"
    r"в\s+размере\s+" + PERCENT_PATTERN + r".{0,200}?"
    r"равную\s+"
    rf"({NUMBER_PATTERN})"
    r"(?:\s*тенге)?",
    re.IGNORECASE | re.DOTALL,
)

GuaranteeType = Literal["OBLIGATIONS", "ANTIDUMPING", "ADVANCE"]

GUARANTEE_PATTERNS = {
    "OBLIGATIONS": OBLIGATIONS_PATTERN,
    "ANTIDUMPING": ANTIDUMPING_PATTERN,
    "ADVANCE": ADVANCE_PATTERN,
}


def _normalize(text: str) -> str:
    return re.sub(r"[ \t]+", " ", text)


def iter_pages_text(contract_content: bytes):
    doc = pymupdf.open(stream=contract_content, filetype="pdf")
    try:
        for page in doc:
            yield _normalize(page.get_text())  # type: ignore
    finally:
        doc.close()


def extract_guarantee_amount(
    contract_content: bytes, guarantee_amount_pattern: re.Pattern
) -> str | None:
    window: deque[str] = deque(maxlen=3)

    for page in iter_pages_text(contract_content):
        window.append(page)
        merged = "\n".join(window)
        matched = guarantee_amount_pattern.search(merged)
        if matched is not None:
            try:
                guarantee_amount = re.sub("\s", "", matched.group(1))
                if re.match(r"\A\d+(?:[.,]\d+)?\Z", guarantee_amount):
                    return guarantee_amount
            except IndexError:
                continue

    logger.warning(
        "Guarantee amount was not found in contract content: pattern=%s",
        guarantee_amount_pattern.pattern,
    )
    return None

async def extract_download_link_from_page(registry_number: int, http_provider: DirectusHttpProvider) :
    response = await http_provider.get(
        f'https://old.goszakup.gov.kz/ru/egzcontract/cpublic/contract/{registry_number}'
    )
    tree = html.fromstring(await response.text())

    table = tree.xpath('//table[@id="show_doc_block1"]/tbody/tr[1]/td[1]/a')
    if not table:
        logger.warning(
            "Download link table was not found on registry page: registry_number=%s",
            registry_number,
        )
        return {}

    download_link = (table[0]).get('href')

    if not download_link:
        return {}

    return download_link


async def download_contract_content(download_link: str, http_provider: DirectusHttpProvider) -> bytes:
    response = await http_provider.get(
        url=download_link
    )
    return await response.read()


async def fetch_contract_content(
    registry_number: int,
    http_provider: HTTPProvider,
    aio_http_provider: DirectusHttpProvider,
    contract_file_path: str | None = None,
) -> bytes:
    """Забирает содержимое договора: напрямую по `contract_file_path`,
    либо (если путь отсутствует) через страницу реестра госзакупа."""
    if contract_file_path is not None:
        logger.info(
            "Fetching contract content directly by contract_file_path: registry_number=%s, "
            "contract_file_path=%s",
            registry_number,
            contract_file_path,
        )
        response = await http_provider.get(url=contract_file_path)
        return response.content

    download_link = await extract_download_link_from_page(
        registry_number=registry_number, http_provider=aio_http_provider
    )
    if not download_link:
        logger.warning(
            "Could not resolve download link from registry page: registry_number=%s",
            registry_number,
        )
        return b""

    logger.info(
        "Fetching contract content via registry download link: registry_number=%s, "
        "download_link=%s",
        registry_number,
        download_link,
    )
    return await download_contract_content(
        download_link=download_link, http_provider=aio_http_provider
    )


async def resolve_guarantee_amount(
    registry_number: int,
    guarantee_amount_pattern: re.Pattern,
    http_provider: HTTPProvider,
    aio_http_provider: DirectusHttpProvider,
    timeout: float,
    contract_file_path: str | None = None,
) -> str | None:
    """Достает сумму гарантии из содержимого договора, разбирая его в отдельном треде
    с ограничением по времени."""
    contract_file_content = await fetch_contract_content(
        registry_number=registry_number,
        http_provider=http_provider,
        aio_http_provider=aio_http_provider,
        contract_file_path=contract_file_path,
    )

    if not contract_file_content:
        logger.warning(
            "Contract content is empty, skipping amount extraction: registry_number=%s",
            registry_number,
        )
        return None

    try:
        # сам тред если что не умрет по истечении таймаута
        # нагрузка на эндпоинт небольшая и пдф документы относительно маленькие и парсятся быстро,
        # так что нет смысла беспокоиться и заводить отдельный процесс, который можно кильнуть
        return await asyncio.wait_for(
            asyncio.to_thread(
                extract_guarantee_amount,
                contract_file_content,
                guarantee_amount_pattern,
            ),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        raise ExternalServiceUnavailable
