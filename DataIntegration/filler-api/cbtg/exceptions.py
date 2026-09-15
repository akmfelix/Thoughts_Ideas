from app.exceptions import FillerHTTPException


class AdNotFoundException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Объявление с таким номером не найдено",
            status_code_name="adNotFound",
            status_code=200,
        )


class AdStatusNotAllowedException(FillerHTTPException):
    def __init__(
        self,
        status_name,
        status_code_name="adBuyStatusNotAllowed"
    ):
        super().__init__(
            status_name=status_name,
            status_code_name=status_code_name,
            status_code=200,
        )


class GoszakupAdBuyStatusDocsChangedNotAllowedException(AdStatusNotAllowedException):
    def __init__(self):
        super().__init__(
            status_name="По данной закупке изменена документация. Данная закупка - неактуальна. "
                        "По ней нельзя подать заявку.",
            status_code_name="adBuyStatusDocsChangedNotAllowed",
        )


class GoszakupAdBuyStatusNotAllowedException(AdStatusNotAllowedException):
    def __init__(self):
        status_name = "Статус закупки должен быть один из: " \
                        "Опубликовано (прием заявок), " \
                        "Опубликовано (дополнение заявок), " \
                        "Опубликовано (прием ценовых предложений)"
        super().__init__(
            status_name=status_name,
        )


class SamrukAdBuyStatusNotAllowedException(AdStatusNotAllowedException):
    def __init__(self):
        status_name = "Статус закупки должен быть один из: " \
                        "Опубликовано"
        super().__init__(
            status_name=status_name,
        )


class GoszakupAdTradeMethodNotAllowedException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Неподходящий способ закупки",
            status_code_name="adTradeMethodNotAllowed",
            status_code=200,
        )


class FoundMoreThanOneAdException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Совпадение оказалось недостаточно точным, нашлось несколько подходящих по номеру объявлений",
            status_code_name="foundMoreThanOneAd",
            status_code=200,
        )


class TenderNotStartedException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Тендер еще не начался",
            status_code_name="tenderNotStarted",
            status_code=200,
        )


class TenderEndedException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Тендер уже завершен",
            status_code_name="tenderEnded",
            status_code=200,
        )


class HealthCheckNotPassedException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Сервис недоступен",
            status_code_name="serviceUnavailable",
            status_code=400,
        )


AdNotFound = AdNotFoundException()
GoszakupAdBuyStatusNotAllowed = GoszakupAdBuyStatusNotAllowedException()
GoszakupAdBuyStatusDocsChangedNotAllowed = GoszakupAdBuyStatusDocsChangedNotAllowedException()
SamrukAdBuyStatusNotAllowed = SamrukAdBuyStatusNotAllowedException()
GoszakupAdTradeMethodNotAllowed = GoszakupAdTradeMethodNotAllowedException()
FoundMoreThanOneAd = FoundMoreThanOneAdException()
TenderNotStarted = TenderNotStartedException()
TenderEnded = TenderEndedException()
HealthCheckNotPassed = HealthCheckNotPassedException()
