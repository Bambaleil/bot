from telebot.types import Message

from loader import bot


# Эхо хендлер, куда летят текстовые сообщения без указанного состояния
@bot.message_handler(state=None)
def filter_message(message: Message):
    bot.send_message(message.from_user.id, 'Извини, я тебе не понимаю, обратись лучше к команде: /help')
