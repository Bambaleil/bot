from telebot import types


def start_buttons():
    """ Стартовые кнопки на панели бота"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("/help")
    btn2 = types.KeyboardButton("/history")
    markup.add(btn1, btn2)
    return markup
