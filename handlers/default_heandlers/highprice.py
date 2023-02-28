from loguru import logger
from telebot.types import Message

from database.db import Request
from database.db_user import check_user_decorator
from loader import bot
from states.state_user_hotel import UserInfoState


@bot.message_handler(commands=['highprice'])
@check_user_decorator
def highprice(message: Message, user_request: Request) -> None:
    """ Команда предложения отелей по самой высокой цене."""
    logger.info(f'Пользователь задействовал команду /highprice.')
    user_request.command = message.text[1:]
    user_request.save()
    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=message.chat.id)
    bot.send_message(message.from_user.id, "Привет {name}, введите город где будете искать отель."
                     .format(name=message.from_user.full_name))
