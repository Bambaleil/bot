from telebot.types import Message

from loader import bot
from states.state_logic import get_city
from states.state_user_hotel import UserInfoState


@bot.message_handler(commands=['bestdeal'])
def bot_start(message: Message):
    """ Команда для вывода отелей, наиболее подходящих по цене и расположению от центра """
    bot.set_state(user_id=message.from_user.id, state=UserInfoState.city, chat_id=message.chat.id)
    bot.send_message(message.from_user.id, "Привет, {name} веди город где будете искать отель."
                     .format(name=message.from_user.full_name))
    get_city(message=message)  # функция из файла state_logic


@bot.message_handler(state=UserInfoState.min_price)
def get_min_price(message: Message):
    """ Функция записывает минимальную цену и запрашивает максимальную цену отеля """
    if message.text.isdigit():
        bot.send_message(message.from_user.id, 'Укажите максимальную цену отеля.')
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.max_price, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Цена должна быть написана цифрами.')


@bot.message_handler(state=UserInfoState.max_price)
def get_max_price(message: Message):
    """ Функция записывает максимальную цену и запрашивает дистанцию отеля от центра города """
    if message.text.isdigit():
        bot.send_message(message.from_user.id,
                         'Укажите максимальную дистанцию удаления отеля от центра города в метрах.'
                         )
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.distance, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'Дистанция должна быть написана цифрами.')


@bot.message_handler(state=UserInfoState.distance)
def get_distance(message: Message):
    """ Функция записывает расстояние """
    bot.send_message(message.from_user.id, 'Тут все ваши отели.')
