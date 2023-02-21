from datetime import datetime

from telebot.types import Message

from database.db import Request, History
from database.db_user import autocheck_user


def get_hotels_command(message: Message):
    user: Request = autocheck_user(message.chat)['user']
    new_history: History = History(
        user_id=user,
        command=user.command,
        command_time=datetime.now(),
        currency='USD'
    )
    new_history.save()
    return new_history
