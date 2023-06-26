from loguru import logger
from telebot.types import Message

from database.db import HotelsHistory, History, Request
from loader import bot


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    logger.info('Пользователь задействовал команду /history.')
    bot.send_message(message.from_user.id,
                     f"Привет {message.from_user.full_name}, здесь выводиться 5 последних запросов.")

    user_requests = Request.select().where(Request.user_id == message.from_user.id).order_by(Request.id.desc()).limit(5)
    if not user_requests:
        bot.send_message(message.from_user.id, f'{message.from_user.full_name}, Пока записей историй нету.')
        return

    for user_request in user_requests:
        history_entries = History.select().where(History.user_id == user_request.id).order_by(History.id.desc()).limit(5)
        for entry in history_entries:
            hotels_info = HotelsHistory.select().where(HotelsHistory.history_id == entry.id).order_by(
                HotelsHistory.id.desc())
            hotels = '\n'.join(hotel_info.name for hotel_info in hotels_info) if hotels_info else 'Нет отелей'

            bot.send_message(message.from_user.id, f'Команда: {entry.command}\n'
                                                   f'Дата выполнения: {entry.command_time}\n'
                                                   f'Отели:\n{hotels}')
