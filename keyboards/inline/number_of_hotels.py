from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from recurring_features.state_min_price_2 import state_min_price_2
from loader import bot


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
def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )

    if code == '1':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали один отель.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '2':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали два отеля.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '3':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали три отеля.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '4':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали четыре отеля.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '5':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали пять отелей.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '6':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали шесть отелей.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '7':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали семь отелей.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '8':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали восемь отелей.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '9':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали девять отелей.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
    elif code == '10':
        bot.send_message(callback_query.from_user.id, text='Вы выбрали десять отелей.')
        state_min_price_2(callback_query=callback_query)  # повторяющийся функция изменения состояния на min_price
