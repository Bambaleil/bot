from loguru import logger
from telebot.types import Message, InputMediaPhoto

from loader import bot


@bot.message_handler(content_types=['photo'])
def result(message: Message, info_hotels: list) -> None:
    logger.info('Выводиться результат')
    bot.set_state(user_id=message.chat.id, state=None, chat_id=message.chat.id)
    for hotel in info_hotels:
        if hotel.get('url'):
            media = [InputMediaPhoto(url, caption=f"{hotel['name']}\n"
                                                  f"Адрес: {hotel['adders']}\n"
                                                  f"От центра: {hotel['by_center']} км.\n"
                                                  f"Цена за ночь: {hotel['price']} USD.\n"
                                                  f"Цена за весь период проживания: "
                                                  f"{hotel['price'] * hotel['day_live']} USD.\n"
                                                  f"Сайт: https://www.hotels.com/ho{hotel['id']}\n"
                                                  f"{'-' * 99}") for url in hotel['url']]
            bot.send_media_group(message.chat.id, media)
        else:
            bot.send_message(message.chat.id, f"{hotel['name']}\n"
                                              f"Адрес: {hotel['adders']}\n"
                                              f"От центра: {hotel['by_center']} км.\n"
                                              f"Цена за ночь: {hotel['price']} USD.\n"
                                              f"Цена за весь период проживания: "
                                              f"{hotel['price'] * hotel['day_live']} USD.\n"
                                              f"{'-' * 99}")
