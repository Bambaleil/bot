from loguru import logger
from telebot.types import Message

from database.db_user import check_user_decorator
from database.peewee import Request
from loader import bot
from states.state_user_hotel import UserInfoState


@bot.message_handler(commands=['lowprice'])
@check_user_decorator
def lowprice(message: Message, user_request: Request) -> None:
    """ Команда предложения отелей по самой низкой цене."""
    logger.info(f'Пользователь задействовал команду /lowprice.')
    user_request.command = message.text[1:]
    user_request.save()
    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=message.chat.id)
    bot.send_message(message.from_user.id, "Привет, {name} веди город где будете искать отель."
                     .format(name=message.from_user.full_name))


@bot.message_handler(states=UserInfoState.end_lowprice)
def hostel(message: Message):
    bot.send_message(message.from_user.id, 'Все')
    bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)
