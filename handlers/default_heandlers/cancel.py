from loader import bot


def cancel_world_decorator(func):
    def wrapped(message, *args, **kwargs):
        if message.text == 'cancel':
            bot.set_state(user_id=message.from_user.id, state=None, chat_id=message.chat.id)
            bot.send_message(message.from_user.id, 'Вы отменили опрос для возобновления используйте команды,'
                                                   'которые прописаны в  /help или доступны в меню.')
        else:
            return func(message, *args, **kwargs)

    return wrapped
