from fastapi import HTTPException

error_429 = HTTPException(
    status_code=404,
    detail="Company not found in the database and couldn't query stat.gov.kz API due to 429 Error.",
)

company_404 = HTTPException(
    status_code=404,
    detail="Company not found in the database nor in the stat.gov.kz registry.",
)
