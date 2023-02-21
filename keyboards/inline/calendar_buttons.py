from datetime import date

from loguru import logger
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from database.db_user import check_user_decorator
from database.db import Request
from keyboards.inline.yes_no_buttons import yes_no
from loader import bot
from states.state_user_hotel import UserInfoState


def calendar_2(message: Message) -> None:
    calendar, step = DetailedTelegramCalendar(calendar_id=2, min_date=date.today()).build()
    bot.send_message(message.chat.id, f'Выберите дату выезда {LSTEP[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
@check_user_decorator
def calendar_check_in(call: CallbackQuery, user_request: Request) -> None:
    """ Календарь заезда. Запись заезда. """
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
        logger.info(f'Пользователь выбрал дату заезда {result}')
        user_request.check_in = result
        user_request.save()
        calendar_2(call.message)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
@check_user_decorator
def calendar_check_out(call: CallbackQuery, user_request: Request) -> None:
    """ Календарь выезда. Запись выезда. """
    result, key, step = DetailedTelegramCalendar(locale='ru',
                                                 calendar_id=2,
                                                 min_date=user_request.check_in
                                                 ).process(call.data)
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
        logger.info(f'Пользователь выбрал дату выезда {result}.')
        user_request.check_out = result
        user_request.save()
        bot.set_state(user_id=call.message.chat.id, state=UserInfoState.photo, chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Нужны ли вам фотографии отелей ?', reply_markup=yes_no())
