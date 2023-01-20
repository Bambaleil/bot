from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db_user import check_user_decorator
from database.db import Request
from keyboards.inline import number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


def number_buttons_p() -> InlineKeyboardMarkup:
    """ Клавиатура выбора количества фото, максимум 5 """
    key_bord = InlineKeyboardMarkup(row_width=5)
    bth_1 = InlineKeyboardButton('1', callback_data='button_p_1')
    bth_2 = InlineKeyboardButton('2', callback_data='button_p_2')
    bth_3 = InlineKeyboardButton('3', callback_data='button_p_3')
    bth_4 = InlineKeyboardButton('4', callback_data='button_p_4')
    bth_5 = InlineKeyboardButton('5', callback_data='button_p_5')
    key_bord.add(bth_1, bth_2, bth_3, bth_4, bth_5)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_p_'))
@check_user_decorator
def process_callback_kb1btn1(callback_query: types.CallbackQuery, user_request: Request):
    code = callback_query.data[-1]
    bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    if code == '1':
        logger.info('Пользователь нажал кнопку 1 для фото.')
        user_request.num_photo = 1
        bot.send_message(callback_query.from_user.id, text='Вы выбрали одно фото.')
    elif code == '2':
        logger.info('Пользователь нажал кнопку 2 для фото.')
        user_request.num_photo = 2
        bot.send_message(callback_query.from_user.id, text='Вы выбрали два фото.')
    elif code == '3':
        logger.info('Пользователь нажал кнопку 3 для фото.')
        user_request.num_photo = 3
        bot.send_message(callback_query.from_user.id, text='Вы выбрали три фото.')
    elif code == '4':
        logger.info('Пользователь нажал кнопку 4 для фото.')
        user_request.num_photo = 4
        bot.send_message(callback_query.from_user.id, text='Вы выбрали четыре фото.')
    elif code == '5':
        logger.info('Пользователь нажал кнопку 5 для фото.')
        user_request.num_photo = 5
        bot.send_message(callback_query.from_user.id, text='Вы выбрали пять фото.')
    user_request.save()
    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='Введите количество отелей не больше 10.',
        reply_markup=number_of_hotels.number_buttons_h()
    )
    bot.set_state(
        user_id=callback_query.message.chat.id,
        state=UserInfoState.num_hostels,
        chat_id=callback_query.message.chat.id
    )
