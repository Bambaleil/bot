from loguru import logger
from telebot.types import Message

from database.db import Request
from database.db_user import check_user_decorator
from func_api.func_api import api_request
from func_api.low_high_requests import get_user_by_message
from handlers.default_heandlers.cancel import cancel_world_decorator
from handlers.default_heandlers.result import result
from keyboards.inline import number_of_photo, number_of_hotels
from keyboards.inline.regions_buttons import location_markup
from loader import bot
from states.state_user_hotel import UserInfoState


@bot.message_handler(state=UserInfoState.city)
@cancel_world_decorator
def get_city(message: Message) -> None:
    """ Функция записывает город и спрашивает локацию """
    if message.text.replace(' ', '').replace('-', '').isalpha():
        logger.info(f'Пользователь выбрал город.')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['city'] = message.text
        dict_location = api_request(method_endswith='locations/v3/search',
                                    params={"q": {message.text}, "locale": "ru_RU"},
                                    method_type="GET")
        if len(dict_location) == 0:
            bot.send_message(message.from_user.id, 'Некорректный ввод. Выберите снова команду')
            bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)
        else:
            bot.send_message(message.from_user.id, f'Ваш город {message.text}')
            bot.set_state(user_id=message.from_user.id, state=UserInfoState.location, chat_id=message.chat.id)
            bot.send_message(message.from_user.id, 'Уточните локацию.', reply_markup=location_markup(dict_location))
    else:
        bot.send_message(message.from_user.id, 'Город может содержать только буквы.')


@bot.message_handler(state=UserInfoState.photo)
@cancel_world_decorator
def get_photo(message: Message) -> None:
    """ Функция спрашивает потребность фото для отелей """
    if message.text.lower() == 'да':
        logger.info(f'пользователь написал да.')
        bot.send_message(message.from_user.id, 'Выберите или введите количество фото не больше 5.',
                         reply_markup=number_of_photo.number_buttons_p()
                         )
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_photo, chat_id=message.chat.id)
    elif message.text.lower() == 'нет':
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['num_photo'] = 0
        logger.info(f'пользователь написал нет.')
        bot.send_message(message.from_user.id, 'Выберите или введите количество отелей не больше 10.',
                         reply_markup=number_of_hotels.number_buttons_h()
                         )
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_hostels, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'напишите пожалуйста да или нет.')


@bot.message_handler(state=UserInfoState.num_photo)
@cancel_world_decorator
def get_num_photo(message: Message) -> None:
    """ Функция записывает количество фото для отеля и спрашивает о количестве отелей """
    if message.text in ['1', '2', '3', '4', '5'] and message.text.isdigit():
        logger.info(f'Пользователь выбрал {message.text} фото.')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            data['num_photo'] = int(message.text)
        bot.send_message(message.from_user.id, 'Введите количество отелей не больше 10.',
                         reply_markup=number_of_hotels.number_buttons_h()
                         )
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_hostels, chat_id=message.chat.id)
    else:
        logger.info(f'Пользователь не верно ввел данные')
        bot.send_message(message.from_user.id,
                         f'{"Фото должно быть не больше 5" if message.text.isdigit() else "Вводите только цифры"}.')


@bot.message_handler(state=UserInfoState.num_hostels)
@check_user_decorator
def get_num_hostels(message: Message, user_request: Request) -> None:
    """ Функция записывает количество отелей """
    if message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and message.text.isdigit():
        logger.info(f'Пользователь выбрал {message.text} отелей.')
        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            user_request.city = data['city']
            user_request.location_id = data['id_location']
            user_request.check_in = data['check_in']
            user_request.check_out = data['check_out']
            user_request.num_photo = data['num_photo']
            user_request.num_hostels = int(message.text)
        user_request.save()
        if user_request.command == 'bestdeal':
            bot.set_state(user_id=message.from_user.id, state=UserInfoState.min_price, chat_id=message.chat.id)
            bot.send_message(message.from_user.id, 'Укажите минимальную цену отеля.')
        else:
            bot.send_message(message.from_user.id, "Идет обработка ваших отелей.")
            info_hotels = get_user_by_message(message, user_request)
            result(message, info_hotels)

    else:
        logger.info(f'Пользователь не верно ввел данные')
        bot.send_message(message.from_user.id,
                         f'{"Отелей должно быть не больше 10" if message.text.isdigit() else "Вводите только цифры"}.')
