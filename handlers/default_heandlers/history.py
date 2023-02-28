import sys

from loguru import logger
from telebot.types import Message

from database.db import HotelsHistory, History, Request
from loader import bot


@bot.message_handler(commands=['history'])
def history(message: Message) -> None:
    my_history = list()
    my_user_id = 0
    logger.info('Пользователь задействовал команду /history.')
    bot.send_message(message.from_user.id, f"Привет {message.from_user.full_name},"
                                           f" здесь выводиться 5 последних запросов.")
    user_id = Request.select().order_by(Request.id.desc())
    for id_ in user_id.dicts().execute():
        if int(id_['user_id']) == message.from_user.id:
            my_user_id = id_['id']
    if my_user_id == 0:
        bot.send_message(message.from_user.id, f'{message.from_user.full_name}, Пока записей историй нету.')
        sys.exit()
    command = History.select().where(History.user_id == my_user_id).limit(5).order_by(History.id.desc())
    for com in command.dicts().execute():
        my_history.append({'id': f'{com["id"]}', 'command': f'{com["command"]}', 'date': f'{com["command_time"]}'})
    for id_hotels in my_history:
        history_hotels = HotelsHistory.select().where(HotelsHistory.history_id == id_hotels['id'])\
            .order_by(HotelsHistory.id.desc())
        for item in history_hotels.dicts().execute():
            for info in my_history:
                if int(info['id']) == int(item['history_id']):
                    if info.get('hotel') in my_history:
                        info['hotel'](item['name'])
                    else:
                        info['hotel'] = [item['name']]
    for my_info in my_history:
        bot.send_message(message.from_user.id, f'Команда: {my_info["command"]}\n'
                                               f'Дата выполнения: {my_info["date"]}\n'
                                               f'Отели: {my_info["hotel"] if my_info.get("hotel") else "Нет отелей"}')
