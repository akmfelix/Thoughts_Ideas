from app.exceptions import FillerHTTPException


class ContractNotFoundException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Контракт с таким номером не найден",
            status_code_name="contractNotFound",
            status_code=200,
        )


class FoundMoreThanOneContractException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Нашлось несколько контрактов",
            status_code_name="foundMoreThanOneContract",
            status_code=200,
        )


class FactoringNotFoundException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Факторинг для контракта с таким номером не найден",
            status_code_name="factoringNotFound",
            status_code=200,
        )


FactoringNotFound = FactoringNotFoundException()
ContractNotFound = ContractNotFoundException()
FoundMoreThanOneContract = FoundMoreThanOneContractException()
