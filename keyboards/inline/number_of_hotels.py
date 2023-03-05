from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db import Request
from database.db_user import check_user_decorator
from func_api.low_high_requests import get_user_by_message
from handlers.default_heandlers.result import result
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
    bth_10 = InlineKeyboardButton('10', callback_data='button_h_0')
    key_bord.add(bth_1, bth_2, bth_3, bth_4, bth_5, bth_6, bth_7, bth_8, bth_9, bth_10)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_h_'))
@check_user_decorator
def process_callback_kb1btn1(call: types.CallbackQuery, user_request: Request) -> None:
    code = call.data[-1]
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    if code == '1':
        logger.info('Пользователь нажал кнопку 1 для отеля.')
        num = 1
        user_request.num_hostels = 1
        bot.send_message(call.from_user.id, text='Вы выбрали один отель.')
    elif code == '2':
        logger.info('Пользователь нажал кнопку 2 для отеля.')
        num = 2
        user_request.num_hostels = 2
        bot.send_message(call.from_user.id, text='Вы выбрали два отеля.')
    elif code == '3':
        logger.info('Пользователь нажал кнопку 3 для отеля.')
        num = 3
        user_request.num_hostels = 3
        bot.send_message(call.from_user.id, text='Вы выбрали три отеля.')
    elif code == '4':
        logger.info('Пользователь нажал кнопку 4 для отеля.')
        num = 4
        user_request.num_hostels = 4
        bot.send_message(call.from_user.id, text='Вы выбрали четыре отеля.')
    elif code == '5':
        logger.info('Пользователь нажал кнопку 5 для отеля.')
        num = 5
        user_request.num_hostels = 5
        bot.send_message(call.from_user.id, text='Вы выбрали пять отелей.')
    elif code == '6':
        logger.info('Пользова кнопку 6 для отеля.')
        num = 6
        user_request.num_hostels = 6
        bot.send_message(call.from_user.id, text='Вы выбрали шесть отелей.')
    elif code == '7':
        logger.info('Пользователь нажал кнопку 7 для отеля.')
        num = 7
        user_request.num_hostels = 7
        bot.send_message(call.from_user.id, text='Вы выбрали семь отелей.')
    elif code == '8':
        logger.info('Пользователь нажал кнопку 8 для отеля.')
        num = 8
        user_request.num_hostels = 8
        bot.send_message(call.from_user.id, text='Вы выбрали восемь отелей.')
    elif code == '9':
        logger.info('Пользователь нажал кнопку 9 для отеля.')
        num = 9
        user_request.num_hostels = 9
        bot.send_message(call.from_user.id, text='Вы выбрали девять отелей.')
    elif code == '0':
        logger.info('Пользователь нажал кнопку 10 для отеля.')
        num = 10
        user_request.num_hostels = 10
        bot.send_message(call.from_user.id, text='Вы выбрали десять отелей.')
    with bot.retrieve_data(call.message.chat.id) as data:
        print(data['num_photo'])
        user_request.city = data['city']
        user_request.location_id = data['id_location']
        user_request.check_in = data['check_in']
        user_request.check_out = data['check_out']
        user_request.num_photo = data['num_photo']
        user_request.num_hostels = num
    user_request.save()
    if user_request.command == 'bestdeal':
        bot.set_state(user_id=call.from_user.id, state=UserInfoState.min_price)
        bot.send_message(call.from_user.id, 'Укажите минимальную цену отеля.')
    else:
        bot.send_message(call.from_user.id, "Идет обработка ваших отелей.")
        info_hotels = get_user_by_message(call.message, user_request)
        result(call.message, info_hotels)
