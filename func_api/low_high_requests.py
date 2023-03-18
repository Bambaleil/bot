from telebot.types import Message
import datetime
from database.db import Request, HotelsHistory, HotelsPhotos
from database.db_history_command import get_hotels_command
from func_api.func_api import api_request


def get_user_by_message(message: Message, user_request: Request):
    new_history = get_hotels_command(message)
    info_hotels = db_query(message, new_history, user_request)
    return info_hotels


def db_query(message: Message, new_history, user_request):
    location_id = user_request.location_id
    command = user_request.command
    check_in = user_request.check_in
    year, month, day = str(check_in).split('-')
    check_out = user_request.check_out
    year_1, month_1, day_1 = str(check_out).split('-')
    ch_in = datetime.date(int(year), int(month), int(day))
    ch_out = datetime.date(int(year_1), int(month_1), int(day_1))
    num_day = ch_out - ch_in
    num_day = num_day.days
    num_day = int(num_day)
    num_day = (1 if num_day == 0 else num_day)
    num_hotel = user_request.num_hostels
    info_hostels = api_request(method_endswith='properties/v2/list',
                               params={"currency": "USD",
                                       "eapid": 1,
                                       "locale": "ru_RU",
                                       "siteId": 300000001,
                                       "destination": {
                                           "regionId": f"{str(location_id)}"
                                       },
                                       "checkInDate": {
                                           "day": int(day),
                                           "month": int(month),
                                           "year": int(year)
                                       },
                                       "checkOutDate": {
                                           "day": int(day_1),
                                           "month": int(month_1),
                                           "year": int(year_1)
                                       },
                                       "rooms": [{"adults": 2}],
                                       "resultsStartingIndex": 0,
                                       "resultsSize": 200,
                                       "sort": ("PRICE_LOW_TO_HIGH" if command != 'bestdeal' else "DISTANCE"),
                                       "filters": {
                                           "price": {
                                               "max": (
                                                   9999
                                                   if command != 'bestdeal' else user_request.max_price),
                                               "min": (
                                                   1
                                                   if command != 'bestdeal' else user_request.min_price)
                                           }
                                       }
                                       },
                               method_type="POST")
    if command == 'bestdeal':
        distance = user_request.distance / 1.60934
        info_hostels = list(filter(lambda x: x['by_center'] <= distance, info_hostels))
        info_hostels = info_hostels[:num_hotel]
    info_hostels = (info_hostels[::-1][:num_hotel:] if command == 'highprice' else info_hostels[:num_hotel])
    for hotel in info_hostels:
        hotel['day_live'] = num_day
        photo_hotel = api_request(method_endswith='properties/v2/detail',
                                  params={
                                      "currency": "USD",
                                      "eapid": 1,
                                      "locale": "ru_RU",
                                      "siteId": 300000001,
                                      "propertyId": hotel['id']
                                  },
                                  method_type="POST")
        if user_request.num_photo != 0:
            num_photo = user_request.num_photo
            hotel['url'] = photo_hotel[:num_photo]
        hotel['adders'] = photo_hotel[-1]
    for hotel in info_hostels:
        hotel_history: HotelsHistory = HotelsHistory(
            history_id=new_history,
            hotel_id=hotel['id'],
            name=hotel['name'],
            address=hotel['adders'],
            by_center=hotel['by_center'] * 1.6,
            price=hotel['price']
        )
        hotel_history.save()
        if hotel.get('url'):
            for url in hotel['url']:
                hotel_photo: HotelsPhotos = HotelsPhotos(
                    hotel_id=hotel['id'],
                    url=url
                )
                hotel_photo.save()
    return info_hostels
