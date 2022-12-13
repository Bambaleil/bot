from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_buttons() -> ReplyKeyboardMarkup:
    """ Стартовые кнопки на панели бота"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = KeyboardButton("/help")
    btn2 = KeyboardButton("/history")
    markup.add(btn1, btn2)
    return markup
