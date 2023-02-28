from loguru import logger
from telebot.types import Message

from database.db import Request
from database.db_user import check_user_decorator
from func_api.low_high_requests import get_user_by_message
from handlers.default_heandlers.cancel import cancel_world_decorator
from handlers.default_heandlers.result import result
from loader import bot
from states.state_user_hotel import UserInfoState


@bot.message_handler(commands=['bestdeal'])
@check_user_decorator
def bestdeal(message: Message, user_request: Request) -> None:
    """ Команда для вывода отелей, наиболее подходящих по цене и расположению от центра """
    logger.info(f'Пользователь задействовал команду /bestdeal.')
    user_request.command = message.text[1:]
    user_request.save()
    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=message.chat.id)
    bot.send_message(message.from_user.id, "Привет {name}, введите город где будете искать отель."
                     .format(name=message.from_user.full_name))


@bot.message_handler(state=UserInfoState.min_price)
@check_user_decorator
@cancel_world_decorator
def get_min_price(message: Message, user_request: Request) -> None:
    """ Функция записывает минимальную цену и запрашивает максимальную цену отеля """
    if message.text.isdigit() and int(message.text) > 0:
        logger.info(f'Пользователь выбрал сумму {message.text}.')
        user_request.min_price = int(message.text)
        user_request.save()
        bot.send_message(message.from_user.id, 'Укажите максимальную цену отеля.')
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.max_price, chat_id=message.chat.id)
    else:
        logger.info(f'Пользователь ошибся с вводом минимальной цены отеля')
        bot.send_message(message.from_user.id,
                         f'Цена должна быть {"введена цифрами." if message.text.isalpha() else "больше нуля."}')


@bot.message_handler(state=UserInfoState.max_price)
@check_user_decorator
@cancel_world_decorator
def get_max_price(message: Message, user_request: Request) -> None:
    """ Функция записывает максимальную цену и запрашивает дистанцию отеля от центра города """
    if message.text.isdigit() and user_request.min_price <= int(message.text):
        logger.info(f'Пользователь выбрал сумму {message.text}.')
        user_request.max_price = int(message.text)
        user_request.save()
        bot.send_message(message.from_user.id,
                         'Укажите максимальную дистанцию удаления отеля от центра города в километрах.')
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.distance, chat_id=message.chat.id)
    else:
        logger.info('Пользователь ошибся с вводом максимальной цены отеля.')
        bot.send_message(message.from_user.id,
                         f'Цена должна быть {"введена цифрами." if message.text.isalpha() else "больше минимальной цены отеля."}')


@bot.message_handler(state=UserInfoState.distance)
@check_user_decorator
@cancel_world_decorator
def get_distance(message: Message, user_request: Request) -> None:
    """ Бот записывает дистанцию отелей от центра и выдает их. """
    if message.text.isdigit() and int(message.text) > 0:
        logger.info(f'Пользователь выбрал дистанцию {message.text}.')
        user_request.distance = int(message.text)
        user_request.save()
        bot.send_message(message.from_user.id, 'Идет обработка ваших отелей.')
        info_hotels = get_user_by_message(message, user_request)
        result(message, info_hotels)
    else:
        bot.send_message(message.from_user.id,
                         f'Расстояние должно быть {"введено цифрами." if message.text.isalpha() else "больше 0."}')
