from loguru import logger
from telebot import types
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline import number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


def number_buttons_p() -> InlineKeyboardMarkup:
    """ Клавиатура выбора количества фото, максимум 5 """
    key_bord = InlineKeyboardMarkup(row_width=5)
    button = [
        InlineKeyboardButton(str(num), callback_data=f'button_p_{num}') for num in range(1, 6)
    ]
    key_bord.add(*button)
    return key_bord


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_p_'))
def process_callback_kb1btn1(call: types.CallbackQuery):
    code = call.data[-1]
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )
    bot.set_state(
        user_id=call.message.chat.id,
        state=UserInfoState.num_hostels,
        chat_id=call.message.chat.id
    )

    num_map = {
        '1': 'одно',
        '2': 'два',
        '3': 'три',
        '4': 'четыре',
        '5': 'пять'
    }

    num = int(code)
    logger.info(f"Пользователь нажал кнопку {num} для фото.")
    bot.send_message(call.from_user.id, text=f'Вы выбрали {num_map[code]} фото.')

    with bot.retrieve_data(call.message.chat.id) as data:
        data['num_photo'] = num

    bot.send_message(
        chat_id=call.message.chat.id,
        text='Введите количество отелей не больше 10.',
        reply_markup=number_of_hotels.number_buttons_h()
    )