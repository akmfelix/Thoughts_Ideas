from app.exceptions import FillerHTTPException


class UserNotFoundException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Пользователь не найден",
            status_code_name="userNotFound",
            status_code=200,
        )


class NoQueryParamsException(FillerHTTPException):
    def __init__(self):
        super().__init__(
            status_name="Отсутствуют query параметры",
            status_code_name="noQueryParamsProvided",
            status_code=200,
        )


UserNotFound = UserNotFoundException()
NoQueryParams = NoQueryParamsException()
