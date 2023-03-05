from datetime import date

from loguru import logger
from telebot.types import Message, CallbackQuery
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP

from keyboards.inline.yes_no_buttons import yes_no
from loader import bot
from states.state_user_hotel import UserInfoState


def calendar_2(message: Message) -> None:
    calendar, step = DetailedTelegramCalendar(calendar_id=2, min_date=date.today()).build()
    bot.send_message(message.chat.id, f'Выберите дату выезда {LSTEP[step]}', reply_markup=calendar)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=1))
def calendar_check_in(call: CallbackQuery) -> None:
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
        with bot.retrieve_data(call.message.chat.id) as data:
            data['check_in'] = result
        calendar_2(call.message)


@bot.callback_query_handler(func=DetailedTelegramCalendar.func(calendar_id=2))
def calendar_check_out(call: CallbackQuery) -> None:
    """ Календарь выезда. Запись выезда. """
    with bot.retrieve_data(call.message.chat.id) as data:
        check_in = data['check_in']
    result, key, step = DetailedTelegramCalendar(locale='ru',
                                                 calendar_id=2,
                                                 min_date=check_in).process(call.data)
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
        with bot.retrieve_data(call.message.chat.id) as data:
            data['check_out'] = result
        bot.set_state(user_id=call.message.chat.id, state=UserInfoState.photo, chat_id=call.message.chat.id)
        bot.send_message(call.message.chat.id, 'Нужны ли вам фотографии отелей ?', reply_markup=yes_no())
