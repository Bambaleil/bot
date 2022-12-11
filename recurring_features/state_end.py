from telebot import types

from keyboards.inline import number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


def state_end(callback_query: types.CallbackQuery) -> None:
    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='спасибо за кнопки',
        reply_markup=number_of_hotels.number_buttons_h()
    )
    bot.set_state(
        user_id=callback_query.message.from_user.id,
        state=UserInfoState.num_hostels,
        chat_id=callback_query.message.chat.id
    )