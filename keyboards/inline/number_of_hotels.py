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
    """Клавиатура выбора количества отелей, максимум 10."""
    key_board = InlineKeyboardMarkup(row_width=5)
    buttons = [
        InlineKeyboardButton(str(num), callback_data=f'button_h_{num}') for num in range(1, 11)
    ]
    key_board.add(*buttons)
    return key_board


@bot.callback_query_handler(func=lambda c: c.data and c.data.startswith('button_h_'))
@check_user_decorator
def process_callback_kb1btn1(call: types.CallbackQuery, user_request: Request) -> None:
    code = call.data[-1]
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id
    )

    message_mapping = {
        '1': 'Вы выбрали один отель.',
        '2': 'Вы выбрали два отеля.',
        '3': 'Вы выбрали три отеля.',
        '4': 'Вы выбрали четыре отеля.',
        '5': 'Вы выбрали пять отелей.',
        '6': 'Вы выбрали шесть отелей.',
        '7': 'Вы выбрали семь отелей.',
        '8': 'Вы выбрали восемь отелей.',
        '9': 'Вы выбрали девять отелей.',
        '0': 'Вы выбрали десять отелей.'
    }
    bot.send_message(call.from_user.id, text=message_mapping.get(code, ''))

    with bot.retrieve_data(call.message.chat.id) as data:
        user_request.city, user_request.location_id, user_request.check_in,user_request.check_out, user_request.num_photo = (
            data['city'],
            data['id_location'],
            data['check_in'],
            data['check_out'],
            data['num_photo']
        )
    user_request.num_hostels = int(code) if int(code) != 0 else 10
    user_request.save()
    logger.info(f'Пользователь выбрал {user_request.num_hostels} отелей.')

    if user_request.command == 'bestdeal':
        bot.set_state(user_id=call.from_user.id, state=UserInfoState.min_price)
        bot.send_message(call.from_user.id, 'Укажите минимальную цену отеля.')
    else:
        bot.send_message(call.from_user.id, "Идет обработка ваших отелей.")
        info_hotels = get_user_by_message(call.message, user_request)
        result(call.message, info_hotels)
