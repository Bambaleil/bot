from datetime import date

from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from database.db import Request
from database.db_user import check_user_decorator
from loader import bot


def location_markup(dict_city: dict) -> InlineKeyboardMarkup:
    key_bord = InlineKeyboardMarkup()
    for id_location, location in dict_city.items():
        call = location + '_' + id_location + '_'
        key_bord.add(InlineKeyboardButton(text=location, callback_data=call))
    return key_bord


@bot.callback_query_handler(func=lambda call: call.data.endswith('_'))
@check_user_decorator
def process_callback_location(call: types.CallbackQuery, user_request: Request):
    location, id_location, pattern = call.data.split('_')
    logger.info(f'Пользователь выбрал локацию {location}')
    with bot.retrieve_data(call.message.chat.id) as data:
        data['id_location'] = id_location
    user_request.location_id = id_location
    user_request.save()
    bot.send_message(call.from_user.id, f"Ваша локация {location}.")
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

    calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today()).build()
    bot.send_message(call.message.chat.id, f'Выберите дату заезда {LSTEP[step]}', reply_markup=calendar)
