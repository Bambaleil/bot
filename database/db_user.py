from datetime import date

import telebot.types
from loguru import logger
from peewee import DoesNotExist
from telebot.types import CallbackQuery
from telebot.types import Chat
from telebot.types import User

from database.db import Request
from database.db import db


def check_user_decorator(func):
    def wrapper(input_instance: CallbackQuery):
        if isinstance(input_instance, telebot.types.CallbackQuery):
            response = autocheck_user(input_instance.message.chat)
        elif isinstance(input_instance, telebot.types.Message):
            response = autocheck_user(input_instance.from_user)
        else:
            logger.error(f'Ожидался CallbackQuery или Message, пришло {type(input_instance)}')
            return None
        func(input_instance, response['user'])

    return wrapper


def autocheck_user(user_data: User | Chat) -> dict:
    """
    Добавление юзера в БД, если его нет. Если есть - возвращает dict с его параметрами
    :param User | Chat user_data: ид из Message
    :return: dict
    """
    response = dict()
    response['result'] = False
    response['is_new'] = False
    user_id = user_data.id
    with db:
        try:
            exists_user: Request = Request.get(Request.user_id == user_id)
            logger.info(f'Проверяем пользователя с id={user_id}')
        except DoesNotExist:
            logger.info(f'Пользователя id={user_id} не существует. Создаём новую запись...')

            new_user: Request = add_new_user(user_id)

            logger.info(f'{new_user=}')

            if new_user.id > 0:
                exists_user = Request.get(Request.user_id == user_id)
                logger.info(f'Пользователь id={user_id} добавлен в базу')
                response['is_new'] = True
                response['result'] = True
                response['user'] = exists_user
            else:
                response['result'] = False
        else:
            response['result'] = True
            response['user'] = exists_user
            logger.success(f'Пользователь: {exists_user.user_id}')

    return response


def add_new_user(user_id: int) -> Request:
    """
    Добавление юзера в БД
    :param int user_id: ид юзера
    :return:
    """
    new_user: Request = Request(
        user_id=user_id,
        command='',
        city='',
        location_id=0,
        check_in=date.today(),
        check_out=date.today(),
        num_photo=0,
        num_hostels=0,
        min_price=0,
        max_price=0,
        distance=0,
    )

    new_user.save()

    return new_user
