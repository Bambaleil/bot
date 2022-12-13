from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import number_of_photo
from loader import bot
from recurring_features.state_min_price_1 import state_min_price_1
from states.state_user_hotel import UserInfoState


def yes_no() -> InlineKeyboardMarkup:
    """ Клавиатура выбора ответа да или нет """
    key_bord = InlineKeyboardMarkup(row_width=2)
    bth_1 = InlineKeyboardButton('да', callback_data='button_1')
    bth_2 = InlineKeyboardButton('Нет', callback_data='button_2')
    key_bord.add(bth_1, bth_2)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_'))
def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    code = callback_query.data[-1]
    bot.edit_message_reply_markup(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id
    )
    if code == '1':
        bot.send_message(callback_query.from_user.id, text='Нажали да')
        bot.send_message(
            chat_id=callback_query.message.chat.id,
            text='Введите количество фото не больше 5.',
            reply_markup=number_of_photo.number_buttons_p()
        )
        bot.set_state(
            user_id=callback_query.message.chat.id,
            state=UserInfoState.num_photo,
            chat_id=callback_query.message.chat.id
        )
    elif code == '2':
        state_min_price_1(callback_query=callback_query)  # повторяющийся функция изменения состояния min_price
