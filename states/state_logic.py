from loguru import logger
from telebot.types import Message

from database.db_user import check_user_decorator
from database.peewee import Request
from handlers.default_heandlers.cancel import cancel_world_decorator
from keyboards.inline import calendar_buttons
from keyboards.inline import number_of_photo, number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


@bot.message_handler(state=UserInfoState.city)
@check_user_decorator
@cancel_world_decorator
def get_city(message: Message, user_request: Request) -> None:
    """ Функция записывает город и спрашивает локацию """
    if message.text.isalpha():
        logger.info(f'Пользователь выбрал город.')
        user_request.city = message.text
        user_request.save()
        bot.send_message(message.from_user.id, 'Ваш город {city}.'.format(city=message.text))
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.location, chat_id=message.chat.id)
        bot.send_message(message.from_user.id, 'Уточните локацию.')  # Добавить кнопки
    else:
        bot.send_message(message.from_user.id, 'Город может содержать только буквы.')


@bot.message_handler(state=UserInfoState.location)
@check_user_decorator
@cancel_world_decorator
def get_location(message: Message, user_request: Request):
    """ Функция записывает локацию и спрашивает дату заезда """
    user_request.location = message.text
    user_request.save()
    calendar_buttons.calendar_1(message=message)  # функция из calendar_buttons


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
        logger.info(f'пользователь написал нет.')
        bot.send_message(message.from_user.id, 'Выберите или введите количество отелей не больше 10.',
                         reply_markup=number_of_hotels.number_buttons_h()
                         )
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_hostels, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'напишите пожалуйста да или нет.')


@bot.message_handler(state=UserInfoState.num_photo)
@check_user_decorator
@cancel_world_decorator
def get_num_photo(message: Message, user_request: Request) -> None:
    """ Функция записывает количество фото для отеля и спрашивает о количестве отелей """
    if message.text in ['1', '2', '3', '4', '5'] and message.text.isdigit():
        logger.info(f'Пользователь выбрал {message.text} фото.')
        user_request.num_photo = int(message.text)
        user_request.save()
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
@cancel_world_decorator
def get_num_hostels(message: Message, user_request: Request) -> None:
    """ Функция записывает количество отелей """
    if message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] and message.text.isdigit():
        logger.info(f'Пользователь выбрал {message.text} отелей.')
        user_request.num_hostels = int(message.text)
        user_request.save()
        if user_request.command == 'bestdeal':
            bot.set_state(user_id=message.from_user.id, state=UserInfoState.min_price, chat_id=message.chat.id)
            bot.send_message(message.from_user.id, 'Укажите минимальную цену отеля.')
        elif user_request.command == 'lowprice':
            bot.set_state(user_id=message.from_user.id, state=UserInfoState.end_lowprice, chat_id=message.chat.id)
            bot.send_message(message.from_user.id, "Вот тут все ваши отели по минимальной цене.")
        elif user_request.command == 'highprice':
            bot.set_state(user_id=message.from_user.id, state=UserInfoState.end_highprice, chat_id=message.chat.id)
            bot.send_message(message.from_user.id, "Вот тут все ваши отели по максимальной цене.")
    else:
        logger.info(f'Пользователь не верно ввел данные')
        bot.send_message(message.from_user.id,
                         f'{"Отелей должно быть не больше 10" if message.text.isdigit() else "Вводите только цифры"}.')
