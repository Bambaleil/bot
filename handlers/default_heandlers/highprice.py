from telebot.types import Message

from loader import bot
from states.state_logic import get_city
from states.state_user_hotel import UserInfoState


@bot.message_handler(commands=['highprice'])
def highprice(message: Message) -> None:
    """ Команда предложения отелей по самой высокой цене."""

    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=message.chat.id)
    bot.send_message(message.from_user.id, "Привет, {name} веди город где будете искать отель."
                     .format(name=message.from_user.full_name))
    get_city(message=message)  # функция из файла state_logic


@bot.message_handler(state=UserInfoState.min_price)
def get_min_price(message: Message):
    """ Функция записывает минимальную цену и запрашивает максимальную цену отеля """
    bot.send_message(message.from_user.id, "Вот тут все ваши отели.")