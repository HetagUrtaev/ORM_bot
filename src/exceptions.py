

class BookingException(Exception):
    detail = "Произошла внутренняя ошибка приложения"
    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class PhoneAPIError(BookingException):
    detail = "Невозможно получить данные о номере с сайта"

class BinAPIError(BookingException):
    detail = "Невозможно получить данные бин карты с сайта"



