from telebot import types

from keyboards.inline import number_of_hotels
from loader import bot
from states.state_user_hotel import UserInfoState


def state_min_price_1(callback_query: types.CallbackQuery) -> None:  # Тут надо словить команды и сделать разделения
    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='Введите количество отелей не больше 10.',
        reply_markup=number_of_hotels.number_buttons_h()
    )
    bot.set_state(
        user_id=callback_query.message.chat.id,
        state=UserInfoState.min_price,
        chat_id=callback_query.message.chat.id
    )
