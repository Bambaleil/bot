from telebot import types

from keyboards.inline import number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


def state_num_hostel(callback_query: types.CallbackQuery) -> None:
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
