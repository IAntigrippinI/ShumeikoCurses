class BookingSiteException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingSiteException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingSiteException):
    detail = "Не осталось свободных номеров"