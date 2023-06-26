from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import number_of_photo, number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


def yes_no() -> InlineKeyboardMarkup:
    """ Клавиатура выбора ответа да или нет """
    buttons = [
        InlineKeyboardButton('да', callback_data='button_1'),
        InlineKeyboardButton('Нет', callback_data='button_2')
    ]
    key_bord = InlineKeyboardMarkup(row_width=2)
    key_bord.add(*buttons)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_'))
def process_callback_kb1btn1(call: types.CallbackQuery):
    code = call.data[-1]
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

    if code == '1':
        bot.send_message(call.from_user.id, text='Нажали да.')
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Введите количество фото не больше 5.',
            reply_markup=number_of_photo.number_buttons_p()
        )
    elif code == '2':
        with bot.retrieve_data(call.message.chat.id) as data:
            data['num_photo'] = 0
        bot.send_message(
            chat_id=call.message.chat.id,
            text='Введите количество отелей не больше 10.',
            reply_markup=number_of_hotels.number_buttons_h()
        )

    bot.set_state(
        user_id=call.message.chat.id,
        state={UserInfoState.num_photo if code == '1' else UserInfoState.num_hostels},
        chat_id=call.message.chat.id
    )
    logger.info(f'пользователь нажал {"да" if code == "1" else "нет"}')
