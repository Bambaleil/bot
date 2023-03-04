import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
RAPID_API_KEY = os.getenv('RAPID_API_KEY')
X_RAPIDAPI_HOST = os.getenv('X_RAPIDAPI_HOST')
DEFAULT_COMMANDS = (
    ('start', "Запустить бота"),
    ('help', "Вывести справку"),
    ('lowprice', "Поиск дешевых отелей"),
    ('highprice', "Поиск дорогих отелей"),
    ('bestdeal', "Вывод отелей, наиболее подходящих по цене и расположению от центра."),
    ('history', "Вывод историю поиска отелей")
)
