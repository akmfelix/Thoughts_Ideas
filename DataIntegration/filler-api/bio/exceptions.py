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


class FailedResponseFromGraphqlException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Возникла ошибка при парсинге ответа от graphQL",
            status_code_name="failedResponseFromGraphql",
            status_code=400,
        )


class MissingContractInfoException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Не был передан contractNumber или contractId в "
                        "параметрах запроса",
            status_code_name="badRequestMissingContractInfo",
            status_code=400,
        )


class ContractNotSupportBioError(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Гарантия исполнения для данного договора не предусмотрена",
            status_code_name="contractNotSupportBioError",
            status_code=200,
        )


class ContractStatusNotAllowedError(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Неподходящий статус договора",
            status_code_name="contractStatusNotAllowed",
            status_code=200,
        )


class ContractTypeNotAllowedError(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Неподходящий тип договора",
            status_code_name="contractTypeNotAllowed",
            status_code=200,
        )


class ContractEndedError(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Срок действия договора уже истёк",
            status_code_name="contractEnded",
            status_code=200,
        )


class ContractEndDateNotAllowedError(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Срок действия договора не должен заканчиваться позднее конца текущего года",
            status_code_name="contractEndDateNotAllowed",
            status_code=200,
        )


ContractEnded = ContractEndedError()
ContractEndDateNotAllowed = ContractEndDateNotAllowedError()
ContractTypeNotAllowed = ContractTypeNotAllowedError()
ContractStatusNotAllowed = ContractStatusNotAllowedError()
ContractNotSupportBio = ContractNotSupportBioError()
ContractNotFound = ContractNotFoundException()
FoundMoreThanOneContract = FoundMoreThanOneContractException()
MissingContractInfo = MissingContractInfoException()
