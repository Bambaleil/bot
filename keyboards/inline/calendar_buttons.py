from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from loader import bot
from telebot.types import Message, CallbackQuery

from datetime import date, datetime
from states.state_user_hotel import UserInfoState


def calendar_1(message: Message) -> None:

    calendar, step = DetailedTelegramCalendar(calendar_id=1, min_date=date.today()).build()
    bot.send_message(message.chat.id, f'Выберите дату заезда {LSTEP[step]}', reply_markup=calendar)


def calendar_2(message: Message, result: datetime) -> None:
    calendar, step = DetailedTelegramCalendar(calendar_id=2, min_date=result).build()
    bot.send_message(message.chat.id, f'Выберите дату выезда {LSTEP[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def calendar_check_in(call: CallbackQuery) -> None:
    """ Календарь заезда """
    result, key, step = DetailedTelegramCalendar(calendar_id=1, locale='ru', min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите дату заезда {LSTEP[step]}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key
                              )
    elif result:
        bot.edit_message_text(f'Дата заезда в отель: {result}',
                              call.message.chat.id,
                              call.message.message_id)
        calendar_2(call.message, result)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def calendar_check_out(call: CallbackQuery) -> None:
    """ Календарь выезда """
    result, key, step = DetailedTelegramCalendar(locale='ru', calendar_id=2, min_date=date.today()).process(call.data)
    if not result and key:
        bot.edit_message_text(f'Выберите дату выезда {LSTEP[step]}',
                              call.message.chat.id,
                              call.message.message_id,
                              reply_markup=key
                              )
    elif result:
        bot.edit_message_text(f'Дата выезда из отеля: {result}',
                              call.message.chat.id,
                              call.message.message_id)
        bot.set_state(user_id=call.message.chat.id, state=UserInfoState.photo, chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Нужны ли вам фотографии отелей ?')
