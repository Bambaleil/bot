# Бот для поиска отелей.

[![Picture_bot](https://umi.ru/images/cms/data/blog/01-tg-bot.jpg)](https://t.me/HannuMantanaBot)

## Ввидение

Даныый бот сотоит из пары комманд таких как.

- /start
- /history
- /bestdeal
- /lowprice
- /highprice
- /help

## Начало работы.

Для активации робота нужно идти по заранию заданному пути начиная с команды `/start` и дальше выбор команды по вашему усмотрению

## Описание комманд

| Команнда | Описание |
| ------ | ------ |
| /start | Запустить бота |
| /history | Вывести справку |
| /bestdeal | Вывод отелей, наиболее подходящих по цене и расположению от центра. |
| /lowprice | Поиск дешевых отелей |
| /highprice | Поиск дорогих отелей |
| /help | Вывод историю поиска отелей |

## Использование сторонних библиотек

```sh
pyTelegramBotAPI==4.4.0
python-dotenv==0.19.2
python-telegram-bot-calendar==1.0.5
peewee==3.15.4
loguru==0.6.0
```

## Описание работы

Бот собирает информацию по вашему запросу, после посылает api-запрос на сайт отелей и выдает соответствующее ответы по вашему поиску. Можно выбрать количество отелей и фотографий по ниму.

## Техническая составляющая

Использование бызы данныйх [SQLite](https://www.sqlite.org/index.html), а также сайта [Rapidapi](https://rapidapi.com/).

## Результаты ввывода

```sh
/history
```

[![Picture_command_history]()](https://t.me/HannuMantanaBot)

```sh
/bestdeal
/lowprice
/highprice
```

[![Picture_all_command_result_find_hotel]()](https://t.me/HannuMantanaBot)