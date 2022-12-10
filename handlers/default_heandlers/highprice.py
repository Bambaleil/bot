from loader import bot
from states.state_user_hotel import UserInfoState
from telebot.types import Message


from states.state_logic import get_city


@bot.message_handler(commands=['highprice'])
def highprice(message: Message) -> None:
    """ Команда предложения отелей по самой высокой цене."""

    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=message.chat.id)
    bot.send_message(message.from_user.id, "Привет, {name} веди город где будете искать отель."
                     .format(name=message.from_user.full_name))


get_city  # функция из файла state_logic
