from telebot.types import Message

from database.db import Request, HotelsHistory, HotelsPhotos
from database.db_history_command import get_hotels_command
from database.db_user import check_user_decorator
from func_api.func_api import api_request


@check_user_decorator
def get_user_by_message(message: Message, user_request: Request):
    new_history = get_hotels_command(message)
    db_query(message, new_history, user_request)


def db_query(message: Message, new_history, user_request):
    location_id = user_request.location_id
    check_in = user_request.check_in
    year, month, day = str(check_in).split('-')
    check_out = user_request.check_out
    year_1, month_1, day_1 = str(check_out).split('-')
    num_hotel = user_request.num_hostels
    if user_request.command == 'bestdeal':
        distance = user_request.distance
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
                                       "sort": "PRICE_LOW_TO_HIGH",
                                       "filters": {
                                           "price": {
                                               "max": (
                                                   150
                                                   if user_request.command != 'bestdeal' else user_request.max_price),
                                               "min": (
                                                   10
                                                   if user_request.command != 'bestdeal' else user_request.min_price)
                                           }
                                       }
                                       },
                               method_type="POST")
    if user_request.command == 'highprice':
        info_hostels = info_hostels[:-(num_hotel - 1):-1]
    else:
        info_hostels = info_hostels[:num_hotel]
    if user_request.num_photo != 0:
        num_photo = user_request.num_photo
        for hotel in info_hostels:
            photo_hotel = api_request(method_endswith='properties/v2/detail',
                                      params={
                                          "currency": "USD",
                                          "eapid": 1,
                                          "locale": "ru_RU",
                                          "siteId": 300000001,
                                          "propertyId": hotel['id']
                                      },
                                      method_type="POST")
            hotel['url'] = photo_hotel[:num_photo]
            hotel['adders'] = photo_hotel[-1]
    print(info_hostels)
    for hotel in info_hostels:
        hotel_history: HotelsHistory = HotelsHistory(
            history_id=new_history,
            hotel_id=hotel['id'],
            name=hotel['name'],
            address=hotel['adders'],
            by_center=hotel['by_center'] * 1.60934,
            price=hotel['price']
        )
        hotel_history.save()
        for url in hotel['url']:
            hotel_photo: HotelsPhotos = HotelsPhotos(
                hotel_id=hotel['id'],
                url=url
            )
            hotel_photo.save()
    return info_hostels
