from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['start'])
def bot_start(message: Message):
    bot.reply_to(message, f"Привет, {message.from_user.full_name}!"
                          f"\nМеня зовут Паспорту, и я помогаю найти подходящий отель для вас")

