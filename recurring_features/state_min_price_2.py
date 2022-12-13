from telebot import types

from loader import bot
from states.state_user_hotel import UserInfoState


def state_min_price_2(callback_query: types.CallbackQuery) -> None:  # Тут надо словить команды и сделать разделения
    bot.send_message(
        chat_id=callback_query.message.chat.id,
        text='Укажите минимальную цену отеля.'
    )
    bot.set_state(user_id=callback_query.message.from_user.id,
                  state=UserInfoState.min_price,
                  chat_id=callback_query.message.chat.id)
