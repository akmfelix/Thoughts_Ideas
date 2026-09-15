from app.api.statgov.models import CompanyInformation


def prepare_data(company_info: CompanyInformation) -> list[str]:
    d = company_info.dict()
    if d["register_date"]:
        d["register_date"] = d["register_date"][:10]
    return list(d.values())
