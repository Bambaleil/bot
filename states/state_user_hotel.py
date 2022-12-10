from telebot.handler_backends import State, StatesGroup


class UserInfoState(StatesGroup):
    """
    Класс состояний пользователя (сценарий пользователя).
    city = Город в котором будет искаться отели.
    location = уточнение местоположения в городе
    check_in = Дата заезда.
    check_out = дата выезда.
    photo = нужны ли фото отелей.
    num_photo = Количество фото отеля.
    num_hostels = Количество отелей.
    min_price = Минимальная цена отеля.
    max_price = Максимальная цена отеля.
    """
    city = State()
    location = State()
    check_in = State()
    check_out = State()
    photo = State()
    num_photo = State()
    num_hostels = State()
    min_price = State()
    max_price = State()
