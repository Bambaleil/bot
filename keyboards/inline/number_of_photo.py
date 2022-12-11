from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from loader import bot
from recurring_features.state_num_hostel import state_num_hostel


def number_buttons_p() -> InlineKeyboardMarkup:
    """ Клавиатура выбора количества фото, максимум 5"""
    key_bord = InlineKeyboardMarkup(row_width=5)
    bth_1 = InlineKeyboardButton('1', callback_data='button_p_1')
    bth_2 = InlineKeyboardButton('2', callback_data='button_p_2')
    bth_3 = InlineKeyboardButton('3', callback_data='button_p_3')
    bth_4 = InlineKeyboardButton('4', callback_data='button_p_4')
    bth_5 = InlineKeyboardButton('5', callback_data='button_p_5')
    key_bord.add(bth_1, bth_2, bth_3, bth_4, bth_5)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_p_'))
def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    if code == '1':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали одно фото')
        state_num_hostel(callback_query=callback_query)  # повторяющийся функция изменения состояния num_hostels
    elif code == '2':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали два фото')
        state_num_hostel(callback_query=callback_query)  # повторяющийся функция изменения состояния num_hostels
    elif code == '3':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали три фото')
        state_num_hostel(callback_query=callback_query)  # повторяющийся функция изменения состояния num_hostels
    elif code == '4':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали четыре фото')
        state_num_hostel(callback_query=callback_query)  # повторяющийся функция изменения состояния num_hostels
    elif code == '5':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали пять фото')
        state_num_hostel(callback_query=callback_query)  # повторяющийся функция изменения состояния num_hostels
