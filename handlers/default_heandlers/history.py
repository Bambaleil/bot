from loguru import logger
from telebot.types import Message

from loader import bot


@bot.message_handler(commands=['history'])
def bot_start(message: Message):
    logger.info('Пользователь задействовал команду /history.')
    bot.reply_to(message, 'Привет, я пока ничего не умею (')
    pass