from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db_user import check_user_decorator
from database.peewee import Request
from loader import bot
from states.state_user_hotel import UserInfoState


def number_buttons_h() -> InlineKeyboardMarkup:
    """ Клавиатура выбора количество отелей, максимум 10 """
    key_bord = InlineKeyboardMarkup(row_width=5)
    bth_1 = InlineKeyboardButton('1', callback_data='button_h_1')
    bth_2 = InlineKeyboardButton('2', callback_data='button_h_2')
    bth_3 = InlineKeyboardButton('3', callback_data='button_h_3')
    bth_4 = InlineKeyboardButton('4', callback_data='button_h_4')
    bth_5 = InlineKeyboardButton('5', callback_data='button_h_5')
    bth_6 = InlineKeyboardButton('6', callback_data='button_h_6')
    bth_7 = InlineKeyboardButton('7', callback_data='button_h_7')
    bth_8 = InlineKeyboardButton('8', callback_data='button_h_8')
    bth_9 = InlineKeyboardButton('9', callback_data='button_h_9')
    bth_10 = InlineKeyboardButton('10', callback_data='button_10')
    key_bord.add(bth_1, bth_2, bth_3, bth_4, bth_5, bth_6, bth_7, bth_8, bth_9, bth_10)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_h_'))
@check_user_decorator
def process_callback_kb1btn1(callback_query: types.CallbackQuery, user_request: Request):
    code = callback_query.data[-1]
    bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )
    if code == '1':
        logger.info('Пользователь нажал кнопку 1 для отеля.')
        user_request.num_hostels = 1
        bot.send_message(callback_query.from_user.id, text='Вы выбрали один отель.')
    elif code == '2':
        logger.info('Пользователь нажал кнопку 2 для отеля.')
        user_request.num_hostels = 2
        bot.send_message(callback_query.from_user.id, text='Вы выбрали два отеля.')
    elif code == '3':
        logger.info('Пользователь нажал кнопку 3 для отеля.')
        user_request.num_hostels = 3
        bot.send_message(callback_query.from_user.id, text='Вы выбрали три отеля.')
    elif code == '4':
        logger.info('Пользователь нажал кнопку 4 для отеля.')
        user_request.num_hostels = 4
        bot.send_message(callback_query.from_user.id, text='Вы выбрали четыре отеля.')
    elif code == '5':
        logger.info('Пользователь нажал кнопку 5 для отеля.')
        user_request.num_hostels = 5
        bot.send_message(callback_query.from_user.id, text='Вы выбрали пять отелей.')
    elif code == '6':
        logger.info('Пользователь нажал кнопку 6 для отеля.')
        user_request.num_hostels = 6
        bot.send_message(callback_query.from_user.id, text='Вы выбрали шесть отелей.')
    elif code == '7':
        logger.info('Пользователь нажал кнопку 7 для отеля.')
        user_request.num_hostels = 7
        bot.send_message(callback_query.from_user.id, text='Вы выбрали семь отелей.')
    elif code == '8':
        logger.info('Пользователь нажал кнопку 8 для отеля.')
        user_request.num_hostels = 8
        bot.send_message(callback_query.from_user.id, text='Вы выбрали восемь отелей.')
    elif code == '9':
        logger.info('Пользователь нажал кнопку 9 для отеля.')
        user_request.num_hostels = 9
        bot.send_message(callback_query.from_user.id, text='Вы выбрали девять отелей.')
    elif code == '10':
        logger.info('Пользователь нажал кнопку 10 для отеля.')
        user_request.num_hostels = 10
        bot.send_message(callback_query.from_user.id, text='Вы выбрали десять отелей.')
    user_request.save()
    if user_request.command == 'bestdeal':
        bot.set_state(user_id=callback_query.from_user.id, state=UserInfoState.min_price)
        bot.send_message(callback_query.from_user.id, 'Укажите минимальную цену отеля.')
    elif user_request.command == 'lowprice':
        bot.set_state(user_id=callback_query.from_user.id, state=UserInfoState.end_lowprice)
        bot.send_message(callback_query.from_user.id, "Вот тут все ваши отели по минимальной цене.")
    elif user_request.command == 'highprice':
        bot.set_state(user_id=callback_query.from_user.id, state=UserInfoState.end_highprice)
        bot.send_message(callback_query.from_user.id, "Вот тут все ваши отели по максимальной цене.")
