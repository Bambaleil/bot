from peewee import *
from loguru import logger
import os.path


db_path = "database.db"
db_path = os.path.join('database', db_path)
db = SqliteDatabase(db_path)


class BaseModel(Model):
    """ Базовая модель (содержит primary key) """
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Request(BaseModel):
    """ Модель запроса """
    user_id = CharField()
    command = CharField()
    city = CharField()
    location = IntegerField()
    check_in = DateField()
    check_out = DateField()
    num_photo = IntegerField()
    num_hostels = IntegerField()
    min_price = IntegerField()
    max_price = IntegerField()
    distance = IntegerField()

    class Meta:
        db_table = 'requests'


class History(BaseModel):
    """
    Модель истории запросов пользователя
    """
    user_id = ForeignKeyField(Request)  # User[id]
    command = CharField()
    command_time = DateField()
    currency = CharField()

    class Meta:
        db_table = 'history_commands'


class HotelsHistory(BaseModel):
    """
    Модель отеля, соотносящиеся с историей запросов
    """
    history_id = ForeignKeyField(History)
    hotel_id = IntegerField()
    name = CharField()
    address = CharField()
    by_center = FloatField()
    price = FloatField()

    class Meta:
        db_table = 'history_results'


class HotelsPhotos(BaseModel):
    """
    Модель фоток отелей по hotel_id
    """
    hotel_id = ForeignKeyField(HotelsHistory.hotel_id)
    url = TextField()

    class Meta:
        db_table = 'hotels_photos'


with db:
    tables = [Request, History, HotelsHistory, HotelsPhotos]
    if not all(table.table_exists() for table in tables):
        db.create_tables(tables)
        logger.debug('Таблица созданы успешно')
    else:
        logger.debug('Таблица уже существуют')
