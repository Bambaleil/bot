from telebot.types import Message

from keyboards.reply.start_buttons import start_buttons
from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message) -> None:
    """ Функция, которая запускает бота и выводит стартовое сообщение с кнопками"""

    bot.send_message(message.from_user.id, "Привет, {name}!"
                                           "\nМеня зовут Паспорту, и я помогаю найти подходящий отель для вас"
                     .format(name=message.from_user.full_name), reply_markup=start_buttons())
