class BookingSiteException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(BookingSiteException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(BookingSiteException):
    detail = "Не осталось свободных номеров"


class EmailIsUsedException(BookingSiteException):
    detail = "Пользователь с такой почтой уже существует"


class UniqueKeyAlreadyUsedException(BookingSiteException):
    detail = "Нарушение уникальности записей"