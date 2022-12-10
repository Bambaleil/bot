from telebot.types import Message

from keyboards.inline import calendar_buttons
from loader import bot
from states.state_user_hotel import UserInfoState


@bot.message_handler(state=UserInfoState.city)
def get_city(message: Message) -> None:
    """ Функция записывает город и спрашивает локацию"""

    if message.text.isalpha():
        bot.send_message(message.from_user.id, 'Ваш город {city}.'.format(city=message.text))
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.location, chat_id=message.chat.id)
        bot.send_message(message.from_user.id, 'Уточните локацию')  # Добавить кнопки
    else:
        bot.send_message(message.from_user.id, 'Город может содержать только буквы.')


@bot.message_handler(state=UserInfoState.location)
def get_location(message: Message):
    """ Функция записывает локацию и спрашивает дату заезда"""
    calendar_buttons.calendar_1(message=message)  # функция из calendar_buttons


@bot.message_handler(state=UserInfoState.photo)
def get_photo(message: Message) -> None:
    """ Функция спрашивает потребность фото для отелей """
    if message.text.lower() == 'да':  # Сделать кнопки
        bot.send_message(message.from_user.id, 'Введите количество фото не больше 5.')  # сделать кнопки
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_photo, chat_id=message.chat.id)
    elif message.text.lower() == 'нет':
        bot.send_message(message.from_user.id, 'Введите количество отелей не больше 10.')
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_hostels, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, 'напишите пожалуйста да или нет.')


@bot.message_handler(state=UserInfoState.num_photo)
def get_num_photo(message: Message) -> None:
    """ Функция спрашивает количество фото для отеля """
    if message.text in ['1', '2', '3', '4', '5']:  # допелить кнопки выбора
        bot.send_message(message.from_user.id, 'Введите количество отелей не больше 10.')
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_hostels, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, f'Неправильно попробуй еще раз')


@bot.message_handler(state=UserInfoState.num_hostels)
def get_num_hostels(message: Message) -> None:
    """ Функция спрашивает количество отелей"""

    if message.text in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:  # допелить кнопки выбора
        bot.send_message(message.from_user.id, f'Спасибо')
        bot.set_state(user_id=message.from_user.id, state=UserInfoState.num_hostels, chat_id=message.chat.id)
    else:
        bot.send_message(message.from_user.id, f'Неправильно попробуй еще раз')
